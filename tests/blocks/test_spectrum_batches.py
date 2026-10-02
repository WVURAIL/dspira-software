from datetime import datetime
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import h5py
from gnuradio import blocks, dspira, gr


class SpectrumBatchesTest(unittest.TestCase):
    def calibration(self, prefix="", length=4096):
        return dspira.systemp_calibration(length, "hot", 10e6, 1419e6,
                                          prefix, False, "False", "180", "40", "test")

    def run_calibration(self, block, spectra, capacity=None):
        count = len(spectra) if capacity is None else capacity
        outputs = [np.full((count, block.vec_length), np.nan, np.float32) for _ in range(3)]
        consumed = block.work([spectra], outputs)
        self.assertEqual(consumed, min(len(spectra), count))
        return [output[:consumed].copy() for output in outputs]

    def test_all_modes_match_separate_scheduler_calls(self):
        batched, separate = self.calibration(), self.calibration()
        shape = np.linspace(0.95, 1.05, 4096, dtype=np.float32)
        for mode, values in [("hot", [340, 350, 360]), ("cold", [50, 60, 70]),
                             ("cal", [75, 85, 95]), ("nocal", [10, 20, 30]),
                             ("nocal_nofilter", [1, 2, 3])]:
            with self.subTest(mode=mode):
                batched.set_collect(mode)
                separate.set_collect(mode)
                spectra = np.array([shape * value for value in values], np.float32)
                actual = self.run_calibration(batched, spectra)
                expected = [self.run_calibration(separate, row[None, :]) for row in spectra]
                for port in range(3):
                    np.testing.assert_allclose(actual[port], np.concatenate([x[port] for x in expected]))
                np.testing.assert_array_equal(batched.hot, separate.hot)
                np.testing.assert_array_equal(batched.cold, separate.cold)

    def test_partial_capacity_and_empty_input(self):
        block = self.calibration(length=4)
        block.set_collect("nocal_nofilter")
        spectra = np.arange(12, dtype=np.float32).reshape(3, 4)
        actual = self.run_calibration(block, spectra, capacity=2)
        np.testing.assert_array_equal(actual[0], spectra[:2])
        self.run_calibration(block, spectra[:0])

    def test_one_capture_per_request_uses_first_available_spectrum(self):
        with tempfile.TemporaryDirectory() as directory:
            block = self.calibration(str(Path(directory) / "capture_"), length=4)
            block.set_collect("nocal_nofilter")
            spectra = np.arange(12, dtype=np.float32).reshape(3, 4)
            block.set_spectrumcapture_toggle(True)
            self.run_calibration(block, spectra[:0])
            self.assertTrue(block.spectrumcapture_toggle)
            self.run_calibration(block, spectra)
            self.run_calibration(block, spectra)
            files = list(Path(directory).glob("*.csv"))
            self.assertEqual(len(files), 1)
            np.testing.assert_allclose(np.loadtxt(files[0], delimiter=",")[:, 1], spectra[0])
            np.testing.assert_array_equal(block.spectrum, spectra[-1])

    def sink(self, directory, integration=0, scale=3):
        return dspira.csv_filesink(4, 4e6, 1420e6, str(Path(directory) / "horn_"),
                                   "True", integration, scale, "180", "40", "test")

    def read_spectra(self, directory):
        return np.array([np.loadtxt(p, delimiter=",")[:, 1]
                         for p in sorted(Path(directory).glob("*.csv"))])

    def test_every_spectrum_saved_even_when_clock_repeats(self):
        with tempfile.TemporaryDirectory() as directory:
            block = self.sink(directory)
            spectra = np.arange(20, dtype=np.float32).reshape(5, 4)
            with patch("gnuradio.dspira._spectrum_file.datetime") as clock:
                clock.now.return_value = datetime(2026, 1, 2, 3, 4, 5)
                self.assertEqual(block.work([spectra], []), 5)
                self.assertEqual(block.work([spectra[:1]], []), 1)
            np.testing.assert_array_equal(self.read_spectra(directory), np.concatenate([spectra, spectra[:1]]))

    def test_long_integration_counter_crosses_batch_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            block = self.sink(directory, integration=1)
            spectra = np.arange(28, dtype=np.float32).reshape(7, 4)
            self.assertEqual(block.work([spectra[:2]], []), 2)
            self.assertEqual(block.work([spectra[2:]], []), 5)
            np.testing.assert_array_equal(self.read_spectra(directory), spectra[[2, 5]])
            self.assertEqual(block.N_long_counter, 1)
            block.set_save_toggle("False")
            self.assertEqual(block.work([spectra], []), 7)
            self.assertEqual(block.work([spectra[:0]], []), 0)
            self.assertEqual(len(list(Path(directory).glob("*.csv"))), 2)

    def test_finite_flowgraph_preserves_and_records_every_vector(self):
        with tempfile.TemporaryDirectory() as directory:
            spectra = np.arange(80, dtype=np.float32).reshape(20, 4)
            source = blocks.vector_source_f(spectra.ravel().tolist(), False, 4)
            calibration = self.calibration(length=4)
            calibration.set_collect("nocal_nofilter")
            output = blocks.vector_sink_f(4)
            sink = self.sink(directory)
            flow = gr.top_block()
            flow.connect(source, calibration, output)
            flow.connect(calibration, sink)
            flow.connect((calibration, 1), blocks.null_sink(gr.sizeof_float * 4))
            flow.connect((calibration, 2), blocks.null_sink(gr.sizeof_float * 4))
            flow.run()
            np.testing.assert_array_equal(np.array(output.data()).reshape(-1, 4), spectra)
            np.testing.assert_array_equal(self.read_spectra(directory), spectra)

    def test_hdf5_recording_preserves_vectors_and_frequency_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = str(Path(directory) / "sky.h5")
            spectra = np.arange(80, dtype=np.float32).reshape(20, 4)
            sink = dspira.hdf5_sink(float, 1, 4, "True", filename,
                                     "A180E40", 1414e6, 10e6 / 4, "test")
            flow = gr.top_block()
            flow.connect(blocks.vector_source_f(spectra.ravel().tolist(), False, 4), sink)
            try:
                flow.run()
                sink.h5.flush()
                with h5py.File(filename, "r") as recording:
                    np.testing.assert_array_equal(recording["spectrum"][:], spectra)
                    self.assertEqual(recording["timestamp"].shape, (20, 1))
                    self.assertTrue(np.all(np.isfinite(recording["timestamp"][:])))
                    self.assertEqual(recording.attrs["pointing"], "A180E40")
                    self.assertEqual(recording.attrs["freq_start"], 1414e6)
                    self.assertEqual(recording.attrs["freq_step"], 10e6 / 4)
            finally:
                sink.h5.close()


if __name__ == "__main__":
    unittest.main()

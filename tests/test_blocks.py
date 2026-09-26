from pathlib import Path
import tempfile
import unittest

import numpy as np
import yaml
from gnuradio import dspira


class ClassroomBlocksTest(unittest.TestCase):
    def test_definitions_resolve_to_the_classroom_package(self):
        root = Path(__file__).resolve().parents[1]
        definitions = list((root / "grc").glob("*.block.yml"))
        self.assertEqual(len(definitions), 12)
        for path in definitions:
            definition = yaml.safe_load(path.read_text())
            name = definition["id"].removeprefix("radio_astro_")
            self.assertTrue(callable(getattr(dspira, name)), name)
            self.assertEqual(definition["templates"]["imports"], "from gnuradio import dspira")
            self.assertTrue(definition["templates"]["make"].startswith("dspira."))

    def test_average_handles_a_batch_and_resets(self):
        block = dspira.vector_moving_average(float, 2, 2, False)
        data = np.array([[2, 4], [4, 8], [8, 16]], dtype=np.float32)
        output = np.zeros_like(data)
        self.assertEqual(block.work([data], [output]), 3)
        np.testing.assert_allclose(output, [[2, 4], [3, 6], [6, 12]])
        block.set_reset_integration(True)
        block.work([data[:1]], [output[:1]])
        np.testing.assert_allclose(output[0], data[0])

    def test_calibration_references_and_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            prefix = str(Path(directory) / "spectrum_")
            block = dspira.systemp_calibration(4096, "hot", 10e6, 1419e6,
                                               prefix, False, "False", "0", "90", "test")

            def sample(mode, value):
                block.set_collect(mode)
                output = [np.empty((1, 4096), np.float32) for _ in range(3)]
                self.assertEqual(block.work([np.full((1, 4096), value, np.float32)], output), 1)
                return output[0][0]

            sample("hot", 350)
            hot = block.hot.copy()
            sample("cold", 60)
            np.testing.assert_array_equal(block.hot, hot)
            cold = block.cold.copy()
            np.testing.assert_allclose(sample("cal", 60)[100:-100], 10, atol=1e-5)
            block.set_spectrumcapture_toggle(True)
            np.testing.assert_allclose(sample("cal", 80)[100:-100], 30, atol=1e-5)
            np.testing.assert_array_equal(block.hot, hot)
            np.testing.assert_array_equal(block.cold, cold)
            saved = list(Path(directory).glob("*.csv"))
            self.assertEqual(len(saved), 1)
            data = np.loadtxt(saved[0], delimiter=",")
            self.assertEqual(data.shape, (4096, 2))
            np.testing.assert_allclose(data[100:-100, 1], 30, atol=1e-4)

    def test_csv_capture_uses_the_requested_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            block = dspira.csv_filesink(4, 4e6, 1420e6, str(Path(directory) / "horn_"),
                                       "True", 0, 1, "0", "90", "test")
            self.assertEqual(block.work([np.array([[1, 2, 3, 4]], np.float32)], []), 1)
            saved = list(Path(directory).glob("horn_*.csv"))
            self.assertEqual(len(saved), 1)
            np.testing.assert_allclose(np.loadtxt(saved[0], delimiter=",")[:, 1], [1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main()

"""Exercise the lesson's processing commands with a known synthetic sky."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import h5py
import numpy as np

SCRIPTS = Path(__file__).resolve().parents[2] / "data-processing"
REST_HZ = 1420.40575177e6


class ProcessingPipelineTest(unittest.TestCase):
    def command(self, name, *args, success=True):
        result = subprocess.run([sys.executable, str(SCRIPTS / (name + ".py")), *map(str, args)],
                                cwd=self.work, capture_output=True, text=True, timeout=60,
                                env={**os.environ, "MPLBACKEND": "Agg"})
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result.stdout

    def recording(self, path, spectrum, *, pointing="A180E40", start=1414e6):
        with h5py.File(path, "w") as output:
            output.attrs.update(freq_start=start, freq_step=10e6 / len(spectrum), pointing=pointing)
            output["spectrum"] = np.tile(spectrum, (12, 1)).astype(np.float32)
            output["timestamp"] = (1_750_000_000 + np.repeat(np.arange(6) * 10, 2))[:, None]

    def test_calibration_conversion_mapping_and_power(self):
        with tempfile.TemporaryDirectory() as directory:
            self.work = Path(directory)
            observations = self.work / "observations"
            observations.mkdir()
            n = 4096
            frequency = 1414e6 + np.arange(n) * 10e6 / n
            line = 20 * np.exp(-0.5 * ((frequency - REST_HZ) / 150e3) ** 2)
            self.recording(self.work / "ground.h5", np.full(n, 350.0))
            self.recording(self.work / "cold.h5", np.full(n, 60.0))
            self.recording(observations / "sky.h5", 70 + line)
            self.command("convert_to_temperature", "-g", "ground.h5", "-s", "cold.h5", "-o", "cal.pdf")
            np.testing.assert_allclose(np.loadtxt(self.work / "cal_gain.csv"), 1, rtol=1e-6)
            np.testing.assert_allclose(np.loadtxt(self.work / "cal_Tsys.csv"), 50, rtol=1e-6)
            for name in ("cal_gain.pdf", "cal_Tsys.pdf"):
                self.assertTrue((self.work / name).read_bytes().startswith(b"%PDF"))
            self.command("hdf5_to_csv", "-f", observations / "sky.h5", "-o", "sky.csv")
            converted = np.loadtxt(self.work / "sky.csv", delimiter=",")
            self.assertEqual(converted.shape, (n, 13))
            np.testing.assert_allclose(converted[:, 0], frequency)
            np.testing.assert_allclose(converted[:, 1:], np.tile((70 + line)[:, None], (1, 12)), rtol=1e-6)
            self.command("map_hydrogen_drift", "-d", observations, "-g", "cal_gain.csv", "-t", "cal_Tsys.csv")
            hits = np.loadtxt(self.work / "hitmap_drift.csv", delimiter=",")
            sky = np.loadtxt(self.work / "h1map_drift.csv", delimiter=",")
            self.assertEqual(hits.shape, (128, 64))
            self.assertGreater(np.count_nonzero(hits), 0)
            expected = 20 * np.sqrt(2 * np.pi) * 150e3 / REST_HZ * 299792.458
            np.testing.assert_allclose(sky[hits > 0] / hits[hits > 0], expected, rtol=0.001)
            self.command("map_from_csv", "-d", self.work)
            self.assertTrue((self.work / "gal_map.pdf").read_bytes().startswith(b"%PDF"))
            self.command("plot_total_power", "-d", observations, "-g", "cal_gain.csv", "-t", "cal_Tsys.csv")
            times = np.atleast_1d(np.loadtxt(self.work / "times.csv"))
            power = np.atleast_1d(np.loadtxt(self.work / "total_power.csv"))
            self.assertEqual(times.shape, power.shape)
            self.assertTrue(np.all(np.diff(times) > 0))
            self.assertTrue(np.all(np.isfinite(power) & (power > 0)))
            coordinates = self.command("az_el_to_galactic", "-a", 180, "-e", 40, "-t", 1_750_000_000)
            self.assertIn("Galactic Longitude:", coordinates)
            self.assertIn("Galactic Latitude:", coordinates)

    def test_unusable_recordings_do_not_create_an_empty_map(self):
        for options, message in [({"pointing": "AZ,EL"}, "Could not read a pointing"),
                                 ({"start": 1400e6}, "OUTSIDE the band")]:
            with self.subTest(options=options), tempfile.TemporaryDirectory() as directory:
                self.work = Path(directory)
                self.recording(self.work / "sky.h5", np.ones(512), **options)
                output = self.command("map_hydrogen_drift", "-d", self.work, success=False)
                self.assertIn(message, output)
                self.assertFalse((self.work / "hitmap_drift.csv").exists())
                self.assertFalse((self.work / "h1map_drift.csv").exists())


if __name__ == "__main__":
    unittest.main()

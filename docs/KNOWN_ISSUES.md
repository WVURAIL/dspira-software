# Compatibility and test status

All seven classroom applications generate successfully with GNU Radio 3.10.9.2.
The generated Python also passes syntax checks. These checks do not start a receiver or verify calibration.

## Corrections to the migration report

The earlier unconnected-port errors came from missing Osmocom and LimeSDR block definitions in the test environment.
The receiver connections were already present in the saved flowgraphs.
Both LimeSDR interferometers also had a missing save-toggle option. That default is now fixed.

The spectrometer and interferometer output prefixes no longer point to an author's home directory.
They default to the current user's home directory, with separate filename prefixes for each output.
Set `DSPIRA_OUTPUT_DIR` to an existing writable directory to choose another location.
The experimental lightning detectors still write triggered files to their working directory.

## Reproduced generation environment

Checked September 25, 2026:

| Component | Version or revision |
| --- | --- |
| Ubuntu | 24.04 |
| GNU Radio | 3.10.9.2 |
| gr-osmosdr block definitions | Ubuntu package 0.2.5-2.1build3 |
| gr-limesdr block definitions | Ubuntu package 3.0.1.10.69-3build6 |
| Shared radio astronomy blocks | `cdbda4f577b538c0750b882241f8a36ecc2e88f8` |

The receiver definitions came from Ubuntu packages. Loading those definitions does not test their drivers or hardware.
CI now repeats generation and syntax checks for all seven applications and reports missing definitions explicitly.

## Still needs hardware testing

- Install the shared library and appropriate receiver driver, then verify acquisition with the intended SDR.
- Check receiver settings, sample rates, gains, recording, and saved data.
- Validate hot-load and cold-sky calibration against the documented sequence.
- Record the tested receiver, amplifier, operating system, dependency versions, and test date.

The two interferometers and four lightning detectors remain experimental pending equipment tests.
A successful generation check is not a classroom-ready certification.
Track the remaining work in [issue 1](https://github.com/WVURAIL/dspira-software/issues/1).
The original migration hashes remain in `migration.json` for provenance.

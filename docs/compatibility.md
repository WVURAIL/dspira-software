# Compatibility and test status

All seven classroom applications generate successfully with GNU Radio 3.10.9.2 and the blocks in this repository.
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
| DSPIRA processing blocks | Included here; calibration and CSV batching corrected during the lesson audit |

The receiver definitions came from Ubuntu packages. Loading those definitions does not test their drivers or hardware.
CI now repeats generation and syntax checks for all seven applications and reports missing definitions explicitly.
The DSPIRA package imports and all seven applications generate with the research package absent.
Block tests cover exports, averaging, reference retention, capture, and distinct spectra delivered in scheduler batches.
All 29 teaching examples also generate. Eighteen software-only examples passed brief runtime checks with an offscreen Qt display.
Audio sources, audio sinks, and receivers still need device tests. Generating the moving-average hierarchy does not exercise it alone.
The example catalog records which checks ran.

## Still needs hardware testing

- Install DSPIRA software and the appropriate receiver driver, then verify acquisition with the intended SDR.
- Check receiver settings, sample rates, gains, recording, and saved data.
- Validate hot-load and cold-sky calibration against the documented sequence.
- Record the tested receiver, amplifier, operating system, dependency versions, and test date.

The two interferometers and four lightning detectors remain experimental pending equipment tests.
A successful generation check is not a classroom-ready certification.
Track the remaining work in [issue 1](https://github.com/WVURAIL/dspira-software/issues/1).

## Multi-vector processing

Calibration processes each spectrum in order, preserving separate output rows and the latest hot and cold references.
The CSV sink processes every row and preserves its integration counter across scheduler calls.
Manual capture saves the first processed spectrum after a request, once per request.
CSV timestamps include microseconds; exclusive file creation prevents an earlier capture from being overwritten.
Repeated timestamps advance by a microsecond until the filename is available.
Tests compare batched calibration with individual calls and run a finite GNU Radio recording flowgraph.
See [the regression tests](../tests/blocks/test_spectrum_batches.py) and [issue 2](https://github.com/WVURAIL/dspira-software/issues/2).

## Teaching examples

The XML examples retain their author and license information and import into GNU Radio 3.10.
The lesson audit corrected window constants, FFT sizes, integer decimation, and HDF5 input types.
The FM receivers now convert 2.5 MHz to 250 kHz, then 240 kHz, then 48 kHz audio.
The Pluto example uses GNU Radio's included IIO source at 1421 MHz with a 3.5 MHz sample rate.
Spectrometer examples use `DSPIRA_OUTPUT_DIR` for output. Their HDF5 pointing field must be filled in before observing.

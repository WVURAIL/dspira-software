# DSPIRA software

Classroom telescope applications for DSPIRA. Start with the
[software guide](https://wvurail.org/dspira/software/) on the lessons website.

This repository owns the classroom flowgraphs. The reusable GNU Radio blocks
remain in [gr-radio_astro](https://github.com/WVURAIL/gr-radio_astro).
Install that library once; this repository does not include another copy.
Physical designs belong in [dspira-hardware](https://github.com/WVURAIL/dspira-hardware).

## Applications

| Files in `flowgraphs/` | Purpose |
| --- | --- |
| `spectrometer_w_cal.grc` | Hydrogen-line spectrometer with calibration and recording |
| `interferometer_simpleSpectrometer_Lime_adding.grc` | Two-input adding interferometer for LimeSDR |
| `interferometer_simpleSpectrometer_Lime_multiplying.grc` | Two-input multiplying interferometer for LimeSDR |
| `lightning_detector_*.grc` | Four experimental lightning-detection variants |

The original migration hashes are preserved in `docs/migration.json`.
Subsequent compatibility fixes pass generation checks but are not hardware qualification.
Read [known limitations](docs/KNOWN_ISSUES.md) before
using these applications with a class.

## Get the applications

```sh
git clone https://github.com/WVURAIL/dspira-software.git
cd dspira-software
```

Open a file from `flowgraphs/` in GNU Radio Companion. Install the
[shared blocks](https://github.com/WVURAIL/gr-radio_astro#installing-from-source)
and the driver for your receiver first. The maintained shared library targets
GNU Radio 3.10. The source baseline for this extraction is `9de98c9c8a281293792ae4dfc3910b6dc6c15c81`.
Existing GNU Radio 3.8 instructions belong to the older `gr38` release line.

Review receiver settings and calibration values before running an application.
The spectrometer and interferometers save CSV files in your home directory by default.
Their filename prefixes distinguish spectra, individual horns, and correlation outputs.
To choose another folder before opening GNU Radio Companion:

```sh
mkdir -p "$HOME/dspira-data"
export DSPIRA_OUTPUT_DIR="$HOME/dspira-data"
gnuradio-companion
```

The selected folder must exist and be writable. You can also edit the `prefix` variables in the flowgraph.
Experimental lightning detectors save triggered files in their working directory.

To update this application checkout, run `git pull --ff-only`. Update the shared
library separately when its release notes require it, and rebuild it afterward.
A flowgraph edit does not require rebuilding the library.

## Contribute

Open a pull request here for classroom application changes. Include the GNU Radio
version, receiver model, and a description of the test you performed. Use
`gr-radio_astro` for reusable block changes and `dspira-hardware` for board designs.
Lesson and worksheet contributions belong in [dspira](https://github.com/WVURAIL/dspira).

Run `python3 scripts/check_flowgraphs.py` to check the application catalog.
This validates file structure and dependency declarations without operating a receiver.

On Ubuntu 24.04, install generation dependencies with:

```sh
sudo apt-get install gnuradio gr-osmosdr gr-limesdr python3-yaml
```

Then run `scripts/check_generation.py` with the shared block definitions on `GRC_BLOCKS_PATH`:

```sh
PYTHONNOUSERSITE=1 GRC_BLOCKS_PATH=/path/to/gr-radio_astro/grc /usr/bin/python3 scripts/check_generation.py
```

This generates each application separately and checks its Python syntax. It does not open receiver hardware.
Use the distribution Python environment; incompatible user-installed NumPy versions can prevent GNU Radio from importing.

## History and old links

The application directory history was extracted with `git subtree split`.
The seven source files were moved from `gr-radio_astro/examples/DSPIRA/` to
`flowgraphs/`. They are no longer duplicated on the shared library's main branch.
See [the migration record](docs/migration.json) for original hashes and the
[link map](https://wvurail.org/dspira/repository-map/) for replacement addresses.
Old tagged releases and commit links remain available in the original repository.

## DSP lesson examples

The [institute exercises](examples/institute/) add 29 flowgraphs for signals, Fourier analysis, filters, and receiver demonstrations.
The catalog separates successful generation checks from examples requiring compatibility updates.
These files have one home here and are linked from the DSPIRA lessons website.

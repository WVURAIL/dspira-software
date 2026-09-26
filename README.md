# DSPIRA software

Classroom telescope applications for DSPIRA. Start with the
[software guide](https://wvurail.org/dspira/software/) on the lessons website.
Watch videos on [DSPIRA's YouTube channel](https://www.youtube.com/@dspira).

This repository contains the classroom flowgraphs and all twelve DSPIRA processing blocks.
Install them together from this checkout. A research software checkout is not required.
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

## Install DSPIRA software

These instructions target GNU Radio 3.10 on Ubuntu. Install the dependencies first:

```sh
sudo apt-get update
sudo apt-get install gnuradio-dev gr-osmosdr airspy cmake g++ git python3-h5py python3-matplotlib python3-yaml
```

LimeSDR applications also require `gr-limesdr` and a compatible receiver.
Then clone, build, test, and install:

```sh
git clone https://github.com/WVURAIL/dspira-software.git
cd dspira-software
cmake -S . -B build -DPYTHON_EXECUTABLE=/usr/bin/python3
cmake --build build
ctest --test-dir build --output-on-failure
sudo cmake --install build
python3 -c "from gnuradio import dspira; print(dspira.__file__)"
```

Restart GNU Radio Companion and open `flowgraphs/spectrometer_w_cal.grc`.
The processing blocks appear in its **DSPIRA** category.
The application files and block implementations have one maintained home here.
Older GNU Radio 3.8 instructions apply only to historical releases.

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

Before updating, preserve local receiver settings and edited flowgraphs.
Run `git pull --ff-only`, then repeat the build, test, and install commands above.

## Contribute

Open a pull request here for classroom application changes. Include the GNU Radio
version, receiver model, and a description of the test you performed. Use
this repository for DSPIRA block changes and `dspira-hardware` for board designs.
Lesson and worksheet contributions belong in [dspira](https://github.com/WVURAIL/dspira).

Run `python3 scripts/check_flowgraphs.py` to check the application catalog.
This validates file structure and dependency declarations without operating a receiver.

On Ubuntu 24.04, install generation dependencies with:

```sh
sudo apt-get install gnuradio gr-osmosdr gr-limesdr python3-yaml
```

After installing DSPIRA, run `scripts/check_generation.py` with this checkout's block definitions:

```sh
PYTHONNOUSERSITE=1 GRC_BLOCKS_PATH="$PWD/grc" /usr/bin/python3 scripts/check_generation.py
```

This generates each application separately and checks its Python syntax. It does not open receiver hardware.
Use the distribution Python environment; incompatible user-installed NumPy versions can prevent GNU Radio from importing.

## History and old links

This is the original `gr-dspira` repository, renamed `dspira-software` on September 25, 2026.
The current software and both projects' Git histories are retained here.

The application directory history was extracted with `git subtree split`.
The seven source files were moved from the former `gr-radio_astro/examples/DSPIRA/` directory to `flowgraphs/`.
The twelve DSPIRA blocks and their existing tests followed in a second migration.
They were removed from the research repository's main branch.
See [the migration record](docs/migration.json) for original hashes and the
[link map](https://wvurail.org/dspira/repository-map/) for replacement addresses.
Old tagged releases and commit links remain available in the original repository.
See [block ownership and compatibility](docs/BLOCKS.md) for the remaining identifier conventions.

## DSP lesson examples

The [Fourier series wave explorer](examples/fourier-wave-explorer/) accompanies the classroom Fourier activity.
It retains its original GNU Radio 3.7 format and MIT notice.

The [institute exercises](examples/institute/) add 29 flowgraphs for signals, Fourier analysis, filters, and receiver demonstrations.
The catalog separates successful generation checks from examples requiring compatibility updates.
These files have one home here and are linked from the DSPIRA lessons website.

# Install DSPIRA software


These instructions target GNU Radio 3.10 on Ubuntu. Install the dependencies first:

```sh
sudo apt-get update
sudo apt-get install gnuradio-dev gr-osmosdr airspy cmake g++ git python3-h5py python3-matplotlib python3-yaml python3-ephem
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

Restart GNU Radio Companion and open `applications/spectrometry/calibrated-spectrometer.grc`.
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

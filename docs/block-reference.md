# DSPIRA block ownership

DSPIRA software owns its applications and these twelve Python blocks:

- `chart_recorder`, `comparator`, and `correlate`
- `csv_filesink`, `hdf5_sink`, and `integration`
- `png_print_spectrum`, `powerSpectrum`, and `running_norm_std`
- `systemp_calibration`, `triggered_save_csv`, and `vector_moving_average`

Nine are used by the current applications. The chart recorder, correlator, and
power-spectrum helper are retained classroom components. Their processing code
was moved unchanged, with its original copyright and license notices.

## Existing flowgraphs

The GRC block identifiers still begin with `radio_astro_` so saved flowgraphs
can open without an identifier conversion. The blocks now appear under **DSPIRA**
and generate imports from `gnuradio.dspira`. The research package does not
install these block definitions or implementations.

Reopen and regenerate older `.grc` files after installing DSPIRA software.
Previously generated Python scripts retain their old imports; do not assume
those scripts update when the block package changes. Historical environments
can continue using their matching tagged releases.

If GNU Radio cannot import `dspira`, use the same Python interpreter for CMake
and GNU Radio. Read CMake's install output to locate the installed package.
A custom installation prefix must be on that interpreter's `PYTHONPATH`.

## Research code

[Radio research software](https://github.com/WVURAIL/radio-research-software)
contains the separate NSF Integrate/Detect applications, research blocks, and
transient experiments. It is not part of the DSPIRA installation.
Some historical research bench examples use the HDF5 recorder now owned here.
Those examples can use this installed block without duplicating its implementation.

## File names and compatibility

Python files use lowercase names with underscores, including `power_spectrum.py`.
Both `dspira.power_spectrum` and the existing `dspira.powerSpectrum` entry point work.
The old `gnuradio.dspira.powerSpectrum` module import remains available.

Saved GRC block identifiers remain unchanged, including `radio_astro_powerSpectrum`.
CMake installs that definition under its original filename to replace older installations without duplicate blocks.

# gr-dspira

> **Archived on 2026-08-20.** Use
> [gr-radio_astro](https://github.com/WVURAIL/gr-radio_astro) for maintained
> DSPIRA software.

This repository preserves GNU Radio 3.7-era DSPIRA prototypes developed in
June and July 2018.

## Contents

| Directory | Historical contents |
|---|---|
| `gr-calibration/` | An early `systemp_calibration` out-of-tree module |
| `gr-spectrometer_output/` | Calibration, display, and spectrometer-output prototypes |
| `gr-tutorial/` | A tutorial-generated harmonic-generator experiment |
| `demos/` | The Fourier Series Wave Explorer flowgraph |

## Migration status

The useful calibration work was transferred to `gr-radio_astro` in 2018:

- [`38b7012`](https://github.com/WVURAIL/gr-dspira/commit/38b70128b1da746eea86ff86fa1718273d7ed072)
  introduced `systemp_calibration` here on 2018-07-17.
- The original author moved the equivalent implementation into
  [`gr-radio_astro` commit `ee22815`](https://github.com/WVURAIL/gr-radio_astro/commit/ee2281583fbbb1edd70f7ef9aee71f4299e6dd7d)
  the next day. Its executable Python is unchanged apart from package
  documentation, and its block definition differs only by the package rename.
- That implementation later evolved into the current
  [`systemp_calibration.py`](https://github.com/WVURAIL/gr-radio_astro/blob/main/python/radio_astro/systemp_calibration.py)
  and
  [GNU Radio block definition](https://github.com/WVURAIL/gr-radio_astro/blob/main/grc/radio_astro_systemp_calibration.block.yml).

The HDF5 and spectrometer concepts also survive in maintained or later work in
`gr-radio_astro`. The `spectrometer_display`, `spectrometer_output`, and
`harmonicgenerator` blocks here are incomplete experiments that were not used
by the demo; they remain here for historical reference rather than being added
to the maintained module.

The tracked Fourier Series Wave Explorer is an exact copy of the flowgraph
published with the
[*Making Waves with Fourier*](https://wvurail.org/dspira-lessons/MakingWavesFourier)
lesson. The 2026 comparison found no remaining implementation that needed to
be migrated.

## Compatibility

The out-of-tree modules target GNU Radio 3.7 and Python 2 and do not configure
unchanged with a current GNU Radio/Python 3 toolchain. GNU Radio 3.10.9.2 can
auto-convert the Fourier demo and generate a runnable flowgraph, with warnings
for deprecated blocks. The original file is retained rather than rewritten.

This repository is a historical record and is not supported as current
runtime software.

## Preservation

The original nine-commit history ends at
[`1840bc2`](https://github.com/WVURAIL/gr-dspira/commit/1840bc2fb5a56aa27bd875b5260976fff04e0990)
and remains unchanged. The single archival commit removes 39 generated Python
2 bytecode files; every corresponding source file remains tracked, and the
bytecode remains recoverable from `1840bc2`. No historical source was
modernized or reformatted.

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md) for authorship and [`NOTICE`](NOTICE)
for rights information. The repository includes the GPL-3.0 text in
[`LICENSE`](LICENSE).

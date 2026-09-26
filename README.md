# DSPIRA software

Software for classroom radio telescopes and DSPIRA lessons.
Start with the [website guide](https://wvurail.org/dspira/software/) or [installation instructions](docs/installation.md).
Watch demonstrations on [DSPIRA's YouTube channel](https://www.youtube.com/@dspira).

## Find what you need

| Folder | Contents |
| --- | --- |
| [applications](applications/) | Seven telescope flowgraphs, grouped by observing task |
| [examples](examples/) | 29 teaching flowgraphs, grouped by DSP topic |
| [data-processing](data-processing/) | Calibration, sky maps, coordinate conversion, CSV export, and power plots |
| [python/gnuradio/dspira](python/gnuradio/dspira/) | Twelve GNU Radio processing blocks |
| [grc](grc/) | GNU Radio Companion definitions for those blocks |
| [docs](docs/) | Installation, compatibility, block reference, and file locations |
| [tests](tests/) | Processing-block and observation-data checks |
| [scripts](scripts/) | Catalog and flowgraph validation tools |
| [licenses](licenses/) | Original notices for teaching examples |

Applications and processing blocks install together from this repository.
A research software checkout is not required.
The calibrated spectrometer is in `applications/spectrometry/calibrated-spectrometer.grc`.
Review [compatibility and hardware checks](docs/compatibility.md) before classroom use.

Physical designs belong in [dspira-hardware](https://github.com/WVURAIL/dspira-hardware).
Lessons, worksheets, and sample datasets belong in [dspira](https://github.com/WVURAIL/dspira).
See [contribution instructions](CONTRIBUTING.md) for software changes.

## Naming and earlier paths

Folders, documentation, and flowgraphs use descriptive lowercase names with hyphens.
Python files and GRC definition files use lowercase names with underscores.
Standard names such as `README.md`, `LICENSE`, and `CMakeLists.txt` follow their tool conventions.
Saved GRC identifiers and existing Python entry points remain compatible.

The [file map](docs/file-map.json) lists earlier paths and their current replacements.
Earlier import records remain available in Git history.
This repository retains the original `gr-dspira` history under the `dspira-software` name.

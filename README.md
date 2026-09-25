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

The initial migration preserves all seven files unchanged. It is not a new
hardware qualification. Read [known limitations](docs/KNOWN_ISSUES.md) before
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

Set output folders, receiver settings, and calibration values for your own
computer. Do not run an application unchanged without reviewing those settings.

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

## History and old links

The application directory history was extracted with `git subtree split`.
The seven source files were moved from `gr-radio_astro/examples/DSPIRA/` to
`flowgraphs/`. They are no longer duplicated on the shared library's main branch.
See [the migration record](docs/migration.json) for original hashes and the
[link map](https://wvurail.org/dspira/repository-map/) for replacement addresses.
Old tagged releases and commit links remain available in the original repository.

# Software checks

`blocks/` contains processing-block tests and the original GNU Radio checks.
Run them through CMake as described in the [installation guide](../docs/installation.md).

`data-processing/` checks pointing parsing and the complete processing workflow:

```sh
python3 tests/data-processing/test_parse_pointing.py
MPLBACKEND=Agg python3 tests/data-processing/test_pipeline.py
```

These tests use synthetic data and do not operate receiver hardware.
The pipeline test checks calibration, CSV export, sky mapping, total power, and invalid-input rejection.

# Software checks

`blocks/` contains processing-block tests and the original GNU Radio checks.
Run them through CMake as described in the [installation guide](../docs/installation.md).

`data-processing/` contains the pointing parser checks:

```sh
python3 tests/data-processing/test_parse_pointing.py
```

These tests use synthetic data and do not operate receiver hardware.

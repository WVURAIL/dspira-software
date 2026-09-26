# Contributing

Send telescope application, DSPIRA block, and observation-processing changes here.
Send lessons and worksheets to [dspira](https://github.com/WVURAIL/dspira).
Send physical designs to [dspira-hardware](https://github.com/WVURAIL/dspira-hardware).

## Add or edit files

- Place telescope flowgraphs in the appropriate `applications/` topic folder.
- Place teaching flowgraphs in the appropriate `examples/` topic folder.
- Update the matching `catalog.json` when adding or moving a flowgraph.
- Keep author and license notices with imported material.
- Use lowercase, descriptive names: hyphens for flowgraphs and folders, underscores for Python files.
- Add old-to-new entries in `docs/file-map.json` when moving existing files.
- Update affected lesson links in `dspira` before publishing a move.

Generate folder indexes after changing a catalog:

```sh
python3 scripts/render_catalogs.py
```

## Validate

Follow the [installation guide](docs/installation.md) for GNU Radio dependencies.
Then run:

```sh
python3 scripts/check_flowgraphs.py
python3 scripts/render_catalogs.py --check
cmake -S . -B build -DPYTHON_EXECUTABLE=/usr/bin/python3
cmake --build build
ctest --test-dir build --output-on-failure
python3 tests/data-processing/test_parse_pointing.py
PYTHONNOUSERSITE=1 GRC_BLOCKS_PATH="$PWD/grc" /usr/bin/python3 scripts/check_generation.py --examples
```

Generation checks do not operate receiver hardware.
Include the GNU Radio version, receiver model, and tests performed in a pull request.
Record hardware results separately from generation checks.

# Maintenance tools

Run these commands from the repository root.

| Command | Purpose |
| --- | --- |
| `python3 scripts/check_flowgraphs.py` | Check catalog coverage, local blocks, and file references |
| `python3 scripts/render_catalogs.py` | Update application and example indexes |
| `python3 scripts/render_catalogs.py --check` | Confirm committed indexes match their catalogs |
| `python3 scripts/check_generation.py` | Generate all telescope applications without opening hardware |
| `python3 scripts/check_generation.py --examples` | Also check teaching examples previously marked as passing |

GNU Radio generation requires the dependencies in the [installation guide](../docs/installation.md).

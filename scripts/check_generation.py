#!/usr/bin/env python3
"""Generate and syntax-check flowgraphs without opening a receiver."""
import argparse
import json
from pathlib import Path
import tempfile


def check_graph(platform, path, output):
    data = platform.parse_flow_graph(str(path))
    required = {block["id"] for block in data["blocks"]
                if block.get("states", {}).get("state", "enabled") not in (False, "disabled")}
    missing = sorted(required - platform.blocks.keys())
    if missing:
        raise ValueError("Missing block definitions: " + ", ".join(missing)
                         + ". Install receiver plugins and set GRC_BLOCKS_PATH for DSPIRA blocks.")
    platform.config.hier_block_lib_dir = str(output)
    graph, generated = platform.load_and_generate_flow_graph(str(path), str(output))
    if graph is None:
        raise ValueError("GNU Radio generation failed")
    generated = Path(generated)
    compile(generated.read_text(), str(generated), "exec")
    return graph


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--examples", action="store_true", help="Include examples previously checked successfully")
    args = parser.parse_args()
    from gnuradio import gr
    from gnuradio.grc.core.platform import Platform
    platform = Platform(version=gr.version(),
                        version_parts=(gr.major_version(), gr.api_version(), gr.minor_version()),
                        prefs=gr.prefs())
    platform.build_library()
    root = Path(__file__).resolve().parents[1]
    paths = args.paths or sorted((root / "applications").rglob("*.grc"))
    if args.examples:
        catalog = json.loads((root / "examples/catalog.json").read_text())
        paths += [root / entry["path"] for entry in catalog if entry["generation"] == "passed"]
    print("GNU Radio", gr.version())
    failed = []
    with tempfile.TemporaryDirectory() as temporary:
        for index, path in enumerate(paths):
            output = Path(temporary) / str(index)
            output.mkdir()
            try:
                check_graph(platform, path.resolve(), output)
                print("PASS", path.name)
            except (ValueError, SyntaxError) as error:
                failed.append(path.name)
                print("FAIL", path.name, error)
    print(f"{len(paths) - len(failed)}/{len(paths)} flowgraphs generated and syntax-checked. Receiver operation is not tested.")
    return bool(failed)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the classroom application catalog without operating a receiver."""
from pathlib import Path
import json
import yaml

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "docs/migration.json").read_text())
files = sorted((root / "flowgraphs").glob("*.grc"))
assert files, "No flowgraphs found"
assert set(manifest["sha256"]).issubset({p.name for p in files}), "Migrated application missing"
for path in files:
    graph = yaml.safe_load(path.read_text())
    assert graph["options"]["parameters"]["id"], path
    blocks = graph["blocks"]
    names = [block["name"] for block in blocks]
    assert len(names) == len(set(names)), (path, "duplicate block name")
    for connection in graph.get("connections", []):
        assert connection[0] in names and connection[2] in names, (path, connection)
    assert any(block["id"].startswith("radio_astro_") for block in blocks), (path, "shared dependency missing")
    print(path.name, len(blocks), "blocks")
print(f"Validated {len(files)} classroom flowgraphs. Receiver operation is not tested.")

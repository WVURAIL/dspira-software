#!/usr/bin/env python3
"""Validate software catalogs without operating a receiver."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import yaml

root = Path(__file__).resolve().parents[1]
applications = json.loads((root / "applications/catalog.json").read_text())
examples = json.loads((root / "examples/catalog.json").read_text())
for directory, catalog in [("applications", applications), ("examples", examples)]:
    paths = [entry["path"] for entry in catalog]
    assert paths and len(paths) == len(set(paths)), (directory, "empty or repeated catalog entry")
    actual = {str(path.relative_to(root)) for path in (root / directory).rglob("*.grc")}
    assert set(paths) == actual, (directory, "catalog does not match flowgraphs", set(paths) ^ actual)
for entry in examples:
    path = root / entry["path"]
    assert (root / entry["license"]).is_file(), (path, "license missing")
    assert entry["topic"] == path.parent.name, (path, "wrong topic")
    ET.parse(path)
file_map = json.loads((root / "docs/file-map.json").read_text())["files"]
for old, current in file_map.items():
    assert (root / current).is_file(), (old, "replacement missing", current)
files = [root / entry["path"] for entry in applications]
local_ids = {yaml.safe_load(p.read_text())["id"] for p in (root / "grc").glob("*.block.yml")}
for path in files:
    graph = yaml.safe_load(path.read_text())
    assert graph["options"]["parameters"]["id"], path
    blocks = graph["blocks"]
    names = [block["name"] for block in blocks]
    assert len(names) == len(set(names)), (path, "duplicate block name")
    for connection in graph.get("connections", []):
        assert connection[0] in names and connection[2] in names, (path, connection)
    dependencies = {block["id"] for block in blocks if block["id"].startswith("radio_astro_")}
    assert dependencies and dependencies <= local_ids, (path, "DSPIRA block definition missing")
    print(path.name, len(blocks), "blocks")
print(f"Validated {len(files)} applications and {len(examples)} teaching examples. Receiver operation is not tested.")

#!/usr/bin/env python3
"""Generate the folder indexes from the application and example catalogs."""
import argparse
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = {
    "spectrometry": "Spectrometry",
    "interferometry": "Interferometry",
    "lightning-detection": "Lightning detection",
    "signal-basics": "Signal basics",
    "fourier-analysis": "Fourier analysis",
    "filters": "Filters",
    "modulation": "Mixing and modulation",
    "receivers": "Radio receivers",
    "sampling": "Sampling",
}
STATUS = {"passed": "Passed", "needs-update": "Needs compatibility updates", "not-checked": "Not checked"}


def table(entries, directory, examples=False):
    lines = ["| Flowgraph | Generation check |", "| --- | --- |"]
    for entry in entries:
        path = Path(entry["path"]).relative_to(directory).as_posix()
        lines.append(f"| [{entry['title']}]({path}) | {STATUS[entry['generation']]} |")
    if examples:
        lines += ["", "License notices:", ""]
        for license in sorted({entry["license"] for entry in entries}):
            label = "Institute examples" if "institute" in license else "Fourier wave explorer"
            depth = len(Path(directory).parts)
            lines.append(f"- [{label}]({'../' * depth}{license})")
    return "\n".join(lines) + "\n"


def documents():
    applications = json.loads((ROOT / "applications/catalog.json").read_text())
    examples = json.loads((ROOT / "examples/catalog.json").read_text())
    outputs = {}
    for kind, entries in [("applications", applications), ("examples", examples)]:
        topics = sorted({Path(entry["path"]).parts[1] for entry in entries})
        is_example = kind == "examples"
        if is_example:
            counts = Counter(entry["generation"] for entry in entries)
            intro = (f"# Teaching examples\n\n{len(entries)} flowgraphs grouped by DSP topic.\n"
                     "These retain XML format, author fields, and license notices.\n"
                     "Compatibility fixes allow GNU Radio 3.10 to import and generate the collection.\n\n"
                     f"Recorded generation results: {counts['passed']} passed, {counts['needs-update']} need updates, "
                     f"and {counts['not-checked']} have not been checked.\n"
                     "A generation pass does not verify runtime behavior or receiver hardware.\n")
        else:
            intro = ("# Telescope applications\n\nSeven GNU Radio 3.10 flowgraphs grouped by observing task.\n"
                     "Start with the [installation guide](../docs/installation.md).\n"
                     "Read [compatibility and hardware checks](../docs/compatibility.md) before classroom use.\n"
                     "The interferometers and lightning detectors remain experimental.\n")
        index = intro + "\n| Topic | Flowgraphs |\n| --- | --- |\n"
        for topic in topics:
            subset = [entry for entry in entries if Path(entry['path']).parts[1] == topic]
            index += f"| [{TOPICS[topic]}]({topic}/) | {len(subset)} |\n"
            directory = kind + "/" + topic
            text = f"# {TOPICS[topic]}\n\n[All {kind}](../)\n\n"
            text += "Generation checks do not operate receiver hardware.\n\n"
            text += table(subset, directory, is_example)
            if topic == "filters":
                text += ("\nThe moving-average block is a hierarchical block used by the comparison example.\n"
                         "Its existing `movingavg` identifier is preserved.\n")
            outputs[directory + "/README.md"] = text
        outputs[kind + "/README.md"] = index
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for name, content in documents().items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(name)
        else:
            path.write_text(content)
    if stale:
        print("Indexes need regeneration: " + ", ".join(stale))
        return 1
    print("Catalog indexes are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

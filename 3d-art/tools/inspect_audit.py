#!/usr/bin/env python3
"""Inventory the audit's art outputs without opening browser captures or changing files."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

CORE = ("ART-BIBLE.md", "KIT-SPEC.md", "STYLE-MATRIX.md")
SUPPLEMENT = [
    "docs/UNKNOWNS.md",
    "docs/COVERAGE.md",
    "analysis/styles/styles.json",
    "analysis/palette/summary.md",
    "analysis/rendering/pipeline.md",
    "analysis/geometry/building-language.md",
    "analysis/geometry/metrics.json",
    "analysis/constants.json",
    "analysis/simulation/simulation.md",
    "evidence/styles/capture-report.json",
    "evidence/manifest.json",
]


def digest(root, relative):
    """Hash only named files inside root."""
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 16), b""):
            h.update(chunk)
    return {"path": relative, "bytes": path.stat().st_size, "sha256": h.hexdigest()}


def inventory(root):
    canonical = [f"docs/{name}" for name in CORE]
    items = {rel: digest(root, rel) for rel in canonical + SUPPLEMENT}
    counts = {name: 0 for name in ("overview", "mid", "street", "night")}
    directory = (root / "evidence/styles").resolve()
    manifest_items = None
    manifest = items["evidence/manifest.json"]
    if manifest:
        try:
            index = json.loads(
                (root / manifest["path"]).read_text(encoding="utf-8-sig")
            )
            if isinstance(index, dict) and isinstance(index.get("entries"), list):
                manifest_items = len(index["entries"])
        except (OSError, ValueError, UnicodeError):
            pass
    if directory.is_relative_to(root) and directory.is_dir():
        for style in directory.iterdir():
            if not style.is_dir() or not style.resolve().is_relative_to(directory):
                continue
            for name in counts:
                png = f"evidence/styles/{style.name}/{name}.png"
                p = (root / png).resolve()
                counts[name] += int(p.is_relative_to(directory) and p.is_file())
    return {
        "root": str(root),
        "core_docs_present": all(items[k] for k in canonical),
        "files": [item for item in items.values() if item],
        "missing_expected_paths": [name for name, item in items.items() if not item],
        "expected_style_frame_name_counts": counts,
        "readable_manifest_entry_count": manifest_items,
        "interpretation": (
            "Locator only. File existence does not establish audit completion, "
            "valid evidence, successful captures, or visual review."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_root", nargs="?", type=Path, default=Path("cityrt-audit"))
    root = parser.parse_args().audit_root.resolve()
    if not root.is_dir():
        print(f"Audit root not found: {root}", file=sys.stderr)
        return 1
    print(json.dumps(inventory(root), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

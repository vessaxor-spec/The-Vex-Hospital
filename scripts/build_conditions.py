#!/usr/bin/env python3
"""
Build script for modular conditions registry.

Merges protocol/conditions/*.json into protocol/conditions.json
and validates against protocol.yaml predicates.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS_DIR = ROOT / "protocol" / "conditions"
OUTPUT_PATH = ROOT / "protocol" / "conditions.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    # Load facts
    facts_path = CONDITIONS_DIR / "facts.json"
    if not facts_path.exists():
        print(f"ERROR: {facts_path} not found", file=sys.stderr)
        return 1
    facts = load_json(facts_path)["facts"]

    # Load all condition modules
    all_conditions = {}
    module_files = sorted(CONDITIONS_DIR.glob("*.json"))
    for module_file in module_files:
        if module_file.name == "facts.json":
            continue
        module = load_json(module_file)
        if "conditions" not in module:
            print(f"WARNING: {module_file} missing 'conditions' key", file=sys.stderr)
            continue
        for name, cond in module["conditions"].items():
            if name in all_conditions:
                print(f"ERROR: Duplicate condition name: {name}", file=sys.stderr)
                return 1
            all_conditions[name] = cond

    # Build output
    output = {
        "schema_ref": "./conditions.schema.json",
        "registry_version": "1.0-draft",
        "facts": facts,
        "conditions": all_conditions,
    }

    # Write output
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Built {OUTPUT_PATH} with {len(all_conditions)} conditions from {len(module_files)-1} modules")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

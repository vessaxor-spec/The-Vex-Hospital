#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True)
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    context = json.loads(args.context.read_text(encoding="utf-8"))
    module = importlib.import_module(args.module)

    run_trial = getattr(module, "run_trial", None)
    if not callable(run_trial):
        raise RuntimeError("Adapter does not expose callable run_trial(context).")

    result = run_trial(context)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

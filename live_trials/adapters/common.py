from __future__ import annotations

import copy
import json
from pathlib import Path


def canonical_fixture(context: dict) -> dict:
    repo_root = Path(context["repo_root"])
    manifest = context["manifest"]
    case_id = manifest["case_id"]
    playbook = manifest["playbook"]

    candidates = sorted((repo_root / "evals" / "runs").glob(f"RUN-{case_id}-*.json"))
    for path in candidates:
        run = json.loads(path.read_text(encoding="utf-8"))
        if run["case_id"] == case_id and run["playbook"] == playbook:
            result = copy.deepcopy(run)
            result["run_id"] = f"RUN-{manifest['trial_id']}-MOCK"
            result["agent_class"] = "trial-mock-agent"
            result["environment_class"] = "trial-mock-subprocess"
            return result

    raise RuntimeError(
        f"No canonical fixture for case {case_id} with playbook {playbook}"
    )

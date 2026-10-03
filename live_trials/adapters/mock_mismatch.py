from __future__ import annotations

from live_trials.adapters.common import canonical_fixture


def run_trial(context: dict) -> dict:
    run = canonical_fixture(context)
    run["case_id"] = "EVAL-999"
    return {
        "behavioral_run": run,
        "usage": {
            "cost_usd": 0,
            "requests": 0,
            "tool_actions": 0,
        },
    }

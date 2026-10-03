from __future__ import annotations

import time

from live_trials.adapters.common import canonical_fixture


def run_trial(context: dict) -> dict:
    time.sleep(2)
    return {
        "behavioral_run": canonical_fixture(context),
        "usage": {
            "cost_usd": 0,
            "requests": 0,
            "tool_actions": 0,
        },
    }

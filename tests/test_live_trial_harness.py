from __future__ import annotations

import copy
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_live_trial import (  # noqa: E402
    TrialFailure,
    enforce_adapter_policy,
    execute_trial,
    filtered_environment,
    load_json,
)


MANIFEST = ROOT / "live_trials" / "manifests" / "TRIAL-EVAL-001-MOCK.json"


class LiveTrialHarnessTests(unittest.TestCase):
    def base_manifest(self):
        return load_json(MANIFEST)

    def test_mock_trial_passes_existing_hospital_evaluator(self):
        result = execute_trial(self.base_manifest())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["case_id"], "EVAL-001")
        self.assertEqual(result["playbook"], "GENERIC")
        self.assertEqual(result["usage"]["cost_usd"], 0)

    def test_unknown_adapter_fails(self):
        manifest = self.base_manifest()
        manifest["adapter_id"] = "UNKNOWN"

        with self.assertRaises(TrialFailure):
            execute_trial(manifest)

    def test_network_policy_escalation_fails(self):
        manifest = self.base_manifest()
        manifest["network_access"] = True

        with self.assertRaisesRegex(TrialFailure, "network policy"):
            execute_trial(manifest)

    def test_overbudget_adapter_fails(self):
        manifest = self.base_manifest()
        manifest["adapter_id"] = "MOCK_OVERBUDGET"
        manifest["budgets"]["max_cost_usd"] = 1
        manifest["budgets"]["max_requests"] = 5
        manifest["budgets"]["max_tool_actions"] = 5

        with self.assertRaisesRegex(TrialFailure, "max_cost_usd"):
            execute_trial(manifest)

    def test_timeout_adapter_fails(self):
        manifest = self.base_manifest()
        manifest["adapter_id"] = "MOCK_TIMEOUT"
        manifest["budgets"]["timeout_seconds"] = 1

        with self.assertRaisesRegex(TrialFailure, "timeout_seconds"):
            execute_trial(manifest)

    def test_adapter_case_mismatch_fails(self):
        manifest = self.base_manifest()
        manifest["adapter_id"] = "MOCK_MISMATCH"

        with self.assertRaisesRegex(TrialFailure, "case_id does not match"):
            execute_trial(manifest)

    def test_live_mode_requires_per_run_authorization(self):
        manifest = self.base_manifest()
        manifest["execution_mode"] = "live"
        manifest["network_access"] = True

        adapter = {
            "supports_live": True,
            "requires_network": True,
            "test_only": False,
            "playbooks": ["GENERIC"],
            "credential_env": [],
        }

        with self.assertRaisesRegex(TrialFailure, "per-run operator authorization"):
            enforce_adapter_policy(manifest, adapter, authorize_live=None)

        enforce_adapter_policy(
            manifest,
            adapter,
            authorize_live="AUTH-SYNTHETIC-TEST",
        )

    def test_test_only_adapter_cannot_run_live(self):
        manifest = self.base_manifest()
        manifest["execution_mode"] = "live"

        adapter = {
            "supports_live": True,
            "requires_network": False,
            "test_only": True,
            "playbooks": ["GENERIC"],
            "credential_env": [],
        }

        with self.assertRaisesRegex(TrialFailure, "Test-only adapter"):
            enforce_adapter_policy(
                manifest,
                adapter,
                authorize_live="AUTH-SYNTHETIC-TEST",
            )

    def test_filtered_environment_passes_only_declared_credentials(self):
        adapter = {
            "credential_env": ["VEX_ALLOWED_SECRET"],
        }

        with patch.dict(
            os.environ,
            {
                "VEX_ALLOWED_SECRET": "allowed-value",
                "VEX_UNRELATED_SECRET": "must-not-pass",
            },
            clear=True,
        ):
            env = filtered_environment(adapter, "live")

        self.assertEqual(env["VEX_ALLOWED_SECRET"], "allowed-value")
        self.assertNotIn("VEX_UNRELATED_SECRET", env)

    def test_missing_declared_live_credential_fails(self):
        adapter = {
            "credential_env": ["VEX_REQUIRED_SECRET"],
        }

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(TrialFailure, "Missing live adapter credential"):
                filtered_environment(adapter, "live")


if __name__ == "__main__":
    unittest.main()

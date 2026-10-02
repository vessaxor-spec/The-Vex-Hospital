from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "evaluate_transition_policy.py"

spec = importlib.util.spec_from_file_location("transition_policy", MODULE_PATH)
transition_policy = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(transition_policy)


class TransitionPolicyTests(unittest.TestCase):
    def test_containment_required_allows_containment(self):
        allowed, matched = transition_policy.evaluate_transition(
            "ADMITTED",
            "CONTAINED",
            {"containment_required": True},
        )
        self.assertTrue(allowed)
        self.assertEqual(matched, ["containment_needed"])

    def test_containment_not_required_allows_baseline(self):
        allowed, matched = transition_policy.evaluate_transition(
            "ADMITTED",
            "BASELINING",
            {"containment_required": False},
        )
        self.assertTrue(allowed)
        self.assertEqual(matched, ["containment_not_needed"])

    def test_false_condition_denies_transition(self):
        allowed, _ = transition_policy.evaluate_transition(
            "ADMITTED",
            "CONTAINED",
            {"containment_required": False},
        )
        self.assertFalse(allowed)

    def test_missing_fact_blocks_transition(self):
        with self.assertRaises(transition_policy.PolicyFailure):
            transition_policy.evaluate_transition(
                "ADMITTED",
                "CONTAINED",
                {},
            )

    def test_authorized_treatment_requires_scoped_authorization_when_required(self):
        allowed, _ = transition_policy.evaluate_transition(
            "TREATMENT_PROPOSED",
            "TREATING",
            {
                "explicit_authorization_required": True,
                "authorization_scoped": True,
            },
        )
        self.assertTrue(allowed)

        denied, _ = transition_policy.evaluate_transition(
            "TREATMENT_PROPOSED",
            "TREATING",
            {
                "explicit_authorization_required": True,
                "authorization_scoped": False,
            },
        )
        self.assertFalse(denied)

    def test_treatment_can_proceed_when_explicit_authorization_not_required(self):
        allowed, _ = transition_policy.evaluate_transition(
            "TREATMENT_PROPOSED",
            "TREATING",
            {
                "explicit_authorization_required": False,
                "authorization_scoped": False,
            },
        )
        self.assertTrue(allowed)

    def test_global_blocking_route_can_override_local_false_route(self):
        allowed, matched = transition_policy.evaluate_transition(
            "AWAITING_AUTHORIZATION",
            "BLOCKED",
            {
                "authorization_denied_or_unavailable": False,
                "nonwaivable_blocker": True,
            },
        )
        self.assertTrue(allowed)
        self.assertEqual(matched, ["nonwaivable_safety_or_authority_condition_prevents_continuation"])

    def test_retry_requires_all_compound_facts(self):
        allowed, _ = transition_policy.evaluate_transition(
            "SELF_TESTING",
            "TREATMENT_PROPOSED",
            {
                "self_test_failed": True,
                "diagnosis_valid": True,
                "retry_budget_available": True,
            },
        )
        self.assertTrue(allowed)

        denied, _ = transition_policy.evaluate_transition(
            "SELF_TESTING",
            "TREATMENT_PROPOSED",
            {
                "self_test_failed": True,
                "diagnosis_valid": False,
                "retry_budget_available": True,
            },
        )
        self.assertFalse(denied)

    def test_discharge_recovery_requires_evidence_and_no_blocking_risk(self):
        allowed, _ = transition_policy.evaluate_transition(
            "DISCHARGE_REVIEW",
            "RECOVERED",
            {
                "required_evidence_satisfied": True,
                "blocking_residual_risk": False,
            },
        )
        self.assertTrue(allowed)

        denied, _ = transition_policy.evaluate_transition(
            "DISCHARGE_REVIEW",
            "RECOVERED",
            {
                "required_evidence_satisfied": True,
                "blocking_residual_risk": True,
            },
        )
        self.assertFalse(denied)

    def test_undeclared_transition_is_denied(self):
        allowed, matched = transition_policy.evaluate_transition(
            "DIAGNOSING",
            "TREATING",
            {},
        )
        self.assertFalse(allowed)
        self.assertEqual(matched, [])

    def test_non_boolean_fact_blocks(self):
        with self.assertRaises(transition_policy.PolicyFailure):
            transition_policy.evaluate_transition(
                "ADMITTED",
                "CONTAINED",
                {"containment_required": "yes"},
            )


if __name__ == "__main__":
    unittest.main()

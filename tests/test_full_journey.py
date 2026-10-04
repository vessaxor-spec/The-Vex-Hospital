#!/usr/bin/env python3
"""
Full patient journey integration test.

Simulates the complete clinical pathway:
ADMITTED → CONTAINED → BASELINING → AUTHORITY_MAPPED → DIAGNOSING →
DIAGNOSIS_CONFIRMED → TREATMENT_PROPOSED → AWAITING_AUTHORIZATION →
TREATING → SELF_TESTING → INDEPENDENT_VERIFICATION → ADVERSARIAL_VERIFICATION →
RESILIENCE_VERIFICATION → REGRESSION_REVIEW → DISCHARGE_REVIEW → RECOVERED
"""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_transition_policy import evaluate_transition


def identity(identity_id: str, role: str, kind: str, session_ref: str = "SYN-TEST-SESSION") -> dict:
    return {
        "identity_id": identity_id,
        "identity_kind": kind,
        "role": role,
        "runtime_class": "synthetic-test-runtime",
        "observer_role": "ci_harness",
        "observed_runtime": True,
        "synthetic": True,
        "visibility": "synthetic_public",
        "session_ref": session_ref,
    }


def evidence(
    evidence_id: str,
    kind: str,
    role: str,
    result: str,
    identity_ref: str,
    *,
    fresh_context: bool = False,
) -> dict:
    payload = f"{evidence_id}|{kind}|{role}|{result}"
    return {
        "evidence_id": evidence_id,
        "kind": kind,
        "producer_role": role,
        "producer_identity_ref": identity_ref,
        "subject": "synthetic test evidence",
        "result": result,
        "synthetic": True,
        "visibility": "synthetic_public",
        "integrity": {
            "algorithm": "sha256",
            "digest": "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest(),
            "scope": "synthetic_payload",
            "synthetic_payload": payload,
        },
        "fresh_context": fresh_context,
    }


def declared_transition(protocol, source: str, target: str) -> bool:
    if source not in protocol["states"]:
        return False

    for transition in protocol["transitions"].get(source, []):
        if transition["to"] == target:
            return True

    for transition in protocol["global_transitions"]:
        if transition["from"] == "*" and transition.get("excluding_terminal", False):
            if transition["to"] == target:
                return True

    return False


class FullJourneyTest(unittest.TestCase):
    def setUp(self):
        self.protocol = yaml.safe_load(
            (ROOT / "protocol" / "protocol.yaml").read_text(encoding="utf-8")
        )
        self.conditions = json.loads(
            (ROOT / "protocol" / "conditions.json").read_text(encoding="utf-8")
        )
        self.specialists = yaml.safe_load(
            (ROOT / "specialists" / "registry.yaml").read_text(encoding="utf-8")
        )

    def test_r0_routine_journey(self):
        """Test complete R0 (routine) patient journey."""
        evidence_records = [
            evidence("EV-ADMIT", "repository_inspection", "case_orchestrator", "observed", "ID-ORCHESTRATOR"),
            evidence("EV-CONTAIN", "runtime_observation", "treating_agent", "observed", "ID-PATIENT"),
            evidence("EV-BASELINE", "diagnosis", "treating_agent", "observed", "ID-PATIENT"),
            evidence("EV-AUTH-MAP", "authorization", "authorized_operator", "granted", "ID-OPERATOR"),
            evidence("EV-DIAGNOSE", "diagnosis", "treating_agent", "pass", "ID-PATIENT"),
            evidence("EV-ROOT-CAUSE", "diagnosis", "case_orchestrator", "pass", "ID-ORCHESTRATOR"),
            evidence("EV-TREATMENT-PLAN", "treatment_result", "treating_agent", "pass", "ID-PATIENT"),
            evidence("EV-TREAT-AUTH", "authorization", "authorized_operator", "granted", "ID-OPERATOR"),
            evidence("EV-TREAT", "treatment_result", "treating_agent", "pass", "ID-PATIENT"),
            evidence("EV-SELF-TEST", "self_test", "treating_agent", "pass", "ID-PATIENT"),
            evidence("EV-INDEP", "independent_verification", "independent_verifier", "pass", "ID-VERIFIER", fresh_context=True),
            evidence("EV-ADV", "adversarial_verification", "adversarial_verifier", "pass", "ID-ADVERSARIAL"),
            evidence("EV-RESIL", "resilience_verification", "resilience_verifier", "pass", "ID-RESILIENCE"),
            evidence("EV-REGRESSION", "regression_review", "independent_verifier", "pass", "ID-VERIFIER"),
            evidence("EV-DISCHARGE", "discharge_review", "independent_verifier", "pass", "ID-VERIFIER"),
        ]

        events = [
            {"seq": 1, "type": "state_transition", "from": "ADMITTED", "to": "CONTAINED", "executed": True,
             "condition_facts": {"containment_required": True}},
            {"seq": 2, "type": "state_transition", "from": "CONTAINED", "to": "BASELINING", "executed": True,
             "condition_facts": {"safe_to_observe": True}},
            {"seq": 3, "type": "state_transition", "from": "BASELINING", "to": "AUTHORITY_MAPPED", "executed": True,
             "condition_facts": {"baseline_sufficient": True}},
            {"seq": 4, "type": "state_transition", "from": "AUTHORITY_MAPPED", "to": "DIAGNOSING", "executed": True,
             "condition_facts": {"authority_envelope_established": True}},
            {"seq": 5, "type": "state_transition", "from": "DIAGNOSING", "to": "DIAGNOSIS_CONFIRMED", "executed": True,
             "condition_facts": {"root_cause_confidence_met": True, "evidence_threshold_met": True}},
            {"seq": 6, "type": "state_transition", "from": "DIAGNOSIS_CONFIRMED", "to": "TREATMENT_PROPOSED", "executed": True,
             "condition_facts": {"bounded_treatment_designable": True}},
            {"seq": 7, "type": "state_transition", "from": "TREATMENT_PROPOSED", "to": "AWAITING_AUTHORIZATION", "executed": True,
             "condition_facts": {"explicit_authorization_required": True, "authorization_scoped": False}},
            {"seq": 8, "type": "state_transition", "from": "AWAITING_AUTHORIZATION", "to": "TREATING", "executed": True,
             "condition_facts": {"authorization_scoped": True}},
            {"seq": 9, "type": "state_transition", "from": "TREATING", "to": "SELF_TESTING", "executed": True,
             "condition_facts": {"treatment_completed": True, "treatment_within_authorized_scope": True}},
            {"seq": 10, "type": "state_transition", "from": "SELF_TESTING", "to": "INDEPENDENT_VERIFICATION", "executed": True,
             "condition_facts": {"independent_verification_required": True, "independent_verification_selected": True}},
            {"seq": 11, "type": "state_transition", "from": "INDEPENDENT_VERIFICATION", "to": "ADVERSARIAL_VERIFICATION", "executed": True,
             "condition_facts": {"independent_verification_passed": True, "adversarial_verification_required": True}},
            {"seq": 12, "type": "state_transition", "from": "ADVERSARIAL_VERIFICATION", "to": "RESILIENCE_VERIFICATION", "executed": True,
             "condition_facts": {"adversarial_verification_passed": True, "resilience_verification_required": True}},
            {"seq": 13, "type": "state_transition", "from": "RESILIENCE_VERIFICATION", "to": "REGRESSION_REVIEW", "executed": True,
             "condition_facts": {"resilience_verification_passed": True}},
            {"seq": 14, "type": "state_transition", "from": "REGRESSION_REVIEW", "to": "DISCHARGE_REVIEW", "executed": True,
             "condition_facts": {"required_capabilities_preserved": True, "blocking_regression_present": False}},
            {"seq": 15, "type": "state_transition", "from": "DISCHARGE_REVIEW", "to": "RECOVERED", "executed": True,
             "condition_facts": {"required_evidence_satisfied": True, "blocking_residual_risk": False}},
        ]

        for event in events:
            self.assertTrue(
                declared_transition(self.protocol, event["from"], event["to"]),
                f"Illegal transition: {event['from']} -> {event['to']}"
            )

        declared_facts = set(self.conditions["facts"])
        for event in events:
            if "condition_facts" in event:
                for fact in event["condition_facts"]:
                    self.assertIn(fact, declared_facts, f"Undeclared fact: {fact}")

        from scripts.validate_hospital import load_json
        evidence_schema = load_json(ROOT / "evidence" / "evidence-record.schema.json")
        valid_kinds = set(evidence_schema["properties"]["kind"]["enum"])
        for ev in evidence_records:
            self.assertIn(ev["kind"], valid_kinds, f"Invalid evidence kind: {ev['kind']}")

        valid_roles = set(evidence_schema["properties"]["producer_role"]["enum"])
        for ev in evidence_records:
            self.assertIn(ev["producer_role"], valid_roles, f"Invalid producer role: {ev['producer_role']}")

        print("✓ R0 routine journey validation passed")

    def test_r3_critical_journey(self):
        """Test complete R3 (critical) patient journey with human discharge authorization."""
        evidence_records = [
            evidence("EV-ADMIT", "repository_inspection", "case_orchestrator", "observed", "ID-ORCHESTRATOR"),
            evidence("EV-CONTAIN", "runtime_observation", "treating_agent", "observed", "ID-PATIENT"),
            evidence("EV-BASELINE", "diagnosis", "treating_agent", "observed", "ID-PATIENT"),
            evidence("EV-AUTH-MAP", "authorization", "authorized_operator", "granted", "ID-OPERATOR"),
            evidence("EV-DIAGNOSE", "diagnosis", "treating_agent", "pass", "ID-PATIENT"),
            evidence("EV-ROOT-CAUSE", "diagnosis", "case_orchestrator", "pass", "ID-ORCHESTRATOR"),
            evidence("EV-TREATMENT-PLAN", "treatment_result", "treating_agent", "pass", "ID-PATIENT"),
            evidence("EV-TREAT-AUTH", "authorization", "authorized_operator", "granted", "ID-OPERATOR"),
            evidence("EV-DISCHARGE-AUTH", "authorization", "authorized_operator", "granted", "ID-OPERATOR"),
            evidence("EV-TREAT", "treatment_result", "treating_agent", "pass", "ID-PATIENT"),
            evidence("EV-SELF-TEST", "self_test", "treating_agent", "pass", "ID-PATIENT"),
            evidence("EV-INDEP", "independent_verification", "independent_verifier", "pass", "ID-VERIFIER", fresh_context=True),
            evidence("EV-ADV", "adversarial_verification", "adversarial_verifier", "pass", "ID-ADVERSARIAL"),
            evidence("EV-RESIL", "resilience_verification", "resilience_verifier", "pass", "ID-RESILIENCE"),
            evidence("EV-REGRESSION", "regression_review", "independent_verifier", "pass", "ID-VERIFIER"),
            evidence("EV-DISCHARGE", "discharge_review", "independent_verifier", "pass", "ID-VERIFIER"),
        ]

        events = [
            {"seq": 1, "type": "state_transition", "from": "ADMITTED", "to": "CONTAINED", "executed": True,
             "condition_facts": {"containment_required": True}},
            {"seq": 2, "type": "state_transition", "from": "CONTAINED", "to": "BASELINING", "executed": True,
             "condition_facts": {"safe_to_observe": True}},
            {"seq": 3, "type": "state_transition", "from": "BASELINING", "to": "AUTHORITY_MAPPED", "executed": True,
             "condition_facts": {"baseline_sufficient": True}},
            {"seq": 4, "type": "state_transition", "from": "AUTHORITY_MAPPED", "to": "DIAGNOSING", "executed": True,
             "condition_facts": {"authority_envelope_established": True}},
            {"seq": 5, "type": "state_transition", "from": "DIAGNOSING", "to": "DIAGNOSIS_CONFIRMED", "executed": True,
             "condition_facts": {"root_cause_confidence_met": True, "evidence_threshold_met": True}},
            {"seq": 6, "type": "state_transition", "from": "DIAGNOSIS_CONFIRMED", "to": "TREATMENT_PROPOSED", "executed": True,
             "condition_facts": {"bounded_treatment_designable": True}},
            {"seq": 7, "type": "state_transition", "from": "TREATMENT_PROPOSED", "to": "AWAITING_AUTHORIZATION", "executed": True,
             "condition_facts": {"explicit_authorization_required": True, "authorization_scoped": False}},
            {"seq": 8, "type": "state_transition", "from": "AWAITING_AUTHORIZATION", "to": "TREATING", "executed": True,
             "condition_facts": {"authorization_scoped": True}},
            {"seq": 9, "type": "state_transition", "from": "TREATING", "to": "SELF_TESTING", "executed": True,
             "condition_facts": {"treatment_completed": True, "treatment_within_authorized_scope": True}},
            {"seq": 10, "type": "state_transition", "from": "SELF_TESTING", "to": "INDEPENDENT_VERIFICATION", "executed": True,
             "condition_facts": {"independent_verification_required": True, "independent_verification_selected": True}},
            {"seq": 11, "type": "state_transition", "from": "INDEPENDENT_VERIFICATION", "to": "ADVERSARIAL_VERIFICATION", "executed": True,
             "condition_facts": {"independent_verification_passed": True, "adversarial_verification_required": True}},
            {"seq": 12, "type": "state_transition", "from": "ADVERSARIAL_VERIFICATION", "to": "RESILIENCE_VERIFICATION", "executed": True,
             "condition_facts": {"adversarial_verification_passed": True, "resilience_verification_required": True}},
            {"seq": 13, "type": "state_transition", "from": "RESILIENCE_VERIFICATION", "to": "REGRESSION_REVIEW", "executed": True,
             "condition_facts": {"resilience_verification_passed": True}},
            {"seq": 14, "type": "state_transition", "from": "REGRESSION_REVIEW", "to": "DISCHARGE_REVIEW", "executed": True,
             "condition_facts": {"required_capabilities_preserved": True, "blocking_regression_present": False}},
            {"seq": 15, "type": "state_transition", "from": "DISCHARGE_REVIEW", "to": "RECOVERED", "executed": True,
             "condition_facts": {"required_evidence_satisfied": True, "blocking_residual_risk": False}},
        ]

        for event in events:
            self.assertTrue(
                declared_transition(self.protocol, event["from"], event["to"]),
                f"Illegal transition: {event['from']} -> {event['to']}"
            )

        risk_class = self.protocol["risk_classes"]["R3"]
        self.assertEqual(risk_class["independent_verification"], "required")
        self.assertEqual(risk_class["adversarial_verification"], "required")
        self.assertEqual(risk_class["resilience_verification"], "required")
        self.assertEqual(risk_class["human_discharge_authorization"], "required")
        self.assertTrue(risk_class["explicit_treatment_authorization"])

        print("✓ R3 critical journey validation passed")

    def test_transition_policy_evaluation(self):
        """Test that transition policy engine correctly evaluates all journey transitions."""
        test_cases = [
            ("ADMITTED", "CONTAINED", {"containment_required": True}, True),
            ("ADMITTED", "BASELINING", {"containment_required": False}, True),
            ("ADMITTED", "CONTAINED", {"containment_required": False}, False),
            ("CONTAINED", "BASELINING", {"safe_to_observe": True}, True),
            ("BASELINING", "AUTHORITY_MAPPED", {"baseline_sufficient": True}, True),
            ("AUTHORITY_MAPPED", "DIAGNOSING", {"authority_envelope_established": True}, True),
            ("DIAGNOSING", "DIAGNOSIS_CONFIRMED", {"root_cause_confidence_met": True, "evidence_threshold_met": True}, True),
            ("DIAGNOSIS_CONFIRMED", "TREATMENT_PROPOSED", {"bounded_treatment_designable": True}, True),
            ("TREATMENT_PROPOSED", "AWAITING_AUTHORIZATION", {"explicit_authorization_required": True, "authorization_scoped": False}, True),
            ("AWAITING_AUTHORIZATION", "TREATING", {"authorization_scoped": True}, True),
            ("TREATING", "SELF_TESTING", {"treatment_completed": True, "treatment_within_authorized_scope": True}, True),
            ("SELF_TESTING", "INDEPENDENT_VERIFICATION", {"independent_verification_required": True, "independent_verification_selected": True}, True),
            ("INDEPENDENT_VERIFICATION", "ADVERSARIAL_VERIFICATION", {"independent_verification_passed": True, "adversarial_verification_required": True}, True),
            ("ADVERSARIAL_VERIFICATION", "RESILIENCE_VERIFICATION", {"adversarial_verification_passed": True, "resilience_verification_required": True}, True),
            ("RESILIENCE_VERIFICATION", "REGRESSION_REVIEW", {"resilience_verification_passed": True}, True),
            ("REGRESSION_REVIEW", "DISCHARGE_REVIEW", {"required_capabilities_preserved": True, "blocking_regression_present": False}, True),
            ("DISCHARGE_REVIEW", "RECOVERED", {"required_evidence_satisfied": True, "blocking_residual_risk": False}, True),
        ]

        for source, target, facts, expected in test_cases:
            allowed, matched = evaluate_transition(source, target, facts)
            self.assertEqual(allowed, expected,
                f"Transition {source} -> {target} with facts {facts}: expected {expected}, got {allowed}, matched {matched}")

        print("✓ All transition policy evaluations passed")


if __name__ == "__main__":
    unittest.main()

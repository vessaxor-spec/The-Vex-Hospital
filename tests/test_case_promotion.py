from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import yaml

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_case_promotion import evaluate_case_promotion  # noqa: E402


TEMPLATE = ROOT / "templates" / "case-state.yaml"


def identity_id(role):
    return "ID-TEST-" + role.upper().replace("_", "-")


def identity_for_role(role):
    kind_by_role = {
        "authorized_operator": "human_operator",
        "platform_authority": "platform_authority",
        "case_orchestrator": "agent_runtime",
        "treating_agent": "agent_runtime",
        "independent_verifier": "verifier_runtime",
        "adversarial_verifier": "verifier_runtime",
        "resilience_verifier": "verifier_runtime",
        "runtime": "agent_runtime",
        "tool": "tool_runtime",
        "ci_harness": "ci_runtime",
        "external_evaluator": "ci_runtime",
    }

    item = {
        "identity_id": identity_id(role),
        "identity_kind": kind_by_role[role],
        "role": role,
        "runtime_class": "synthetic-local-promotion-test",
        "observer_role": "ci_harness",
        "observed_runtime": True,
        "synthetic": True,
        "visibility": "local_private",
    }

    if item["identity_kind"] == "agent_runtime":
        item["session_ref"] = "SYN-CASE-TEST-PATIENT"
    elif item["identity_kind"] == "verifier_runtime":
        item["session_ref"] = "SYN-CASE-TEST-" + role.upper().replace("_", "-")

    return item


def evidence(
    evidence_id,
    kind,
    role,
    result,
    *,
    scope=None,
    fresh_context=None,
    case_id="CASE-TEST",
):
    payload = f"{evidence_id}|{kind}|{role}|{result}"
    item = {
        "evidence_id": evidence_id,
        "case_id": case_id,
        "kind": kind,
        "producer_role": role,
        "producer_identity_ref": identity_id(role),
        "subject": "synthetic local promotion test",
        "result": result,
        "synthetic": True,
        "visibility": "local_private",
        "integrity": {
            "algorithm": "sha256",
            "digest": "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest(),
            "scope": "synthetic_payload",
            "synthetic_payload": payload,
        },
    }
    if scope is not None:
        item["scope"] = scope
    if fresh_context is not None:
        item["fresh_context"] = fresh_context
    return item


class CasePromotionEngineTests(unittest.TestCase):
    def base_chart(self):
        chart = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
        chart["case_id"] = "CASE-TEST"
        chart["patient_id"] = "PATIENT-TEST"
        chart["protocol_version"] = "1.0-draft"
        chart["last_updated_at"] = "2026-01-01T00:00:00Z"
        return chart

    def write_chart(self, chart):
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".yaml",
            encoding="utf-8",
            delete=False,
        )
        yaml.safe_dump(chart, handle, sort_keys=False)
        handle.close()
        path = Path(handle.name)
        self.addCleanup(path.unlink)
        return path

    def write_bundle(self, records, case_id="CASE-TEST"):
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            encoding="utf-8",
            delete=False,
        )
        roles = sorted({record["producer_role"] for record in records})
        json.dump(
            {
                "schema_ref": "./evidence-bundle.schema.json",
                "case_id": case_id,
                "identity_attestations": [
                    identity_for_role(role) for role in roles
                ],
                "records": records,
            },
            handle,
            indent=2,
        )
        handle.write("\n")
        handle.close()
        path = Path(handle.name)
        self.addCleanup(path.unlink)
        return path

    def evaluate(self, chart, target, records=None):
        if records is not None:
            identity_refs = set(chart["environment"]["identity_refs"])
            identity_refs.update(
                identity_id(record["producer_role"]) for record in records
            )
            chart["environment"]["identity_refs"] = sorted(identity_refs)

        chart_path = self.write_chart(chart)
        bundle_path = (
            self.write_bundle(records, chart["case_id"])
            if records is not None
            else None
        )
        return evaluate_case_promotion(chart_path, target, bundle_path)

    def test_early_declared_transition_allowed(self):
        chart = self.base_chart()
        chart["current_state"] = "ADMITTED"
        chart["policy_context"]["facts"] = {
            "containment_required": False,
        }

        result = self.evaluate(chart, "BASELINING")
        self.assertEqual(result["decision"], "ALLOWED")

    def test_missing_condition_fact_blocks(self):
        chart = self.base_chart()
        chart["current_state"] = "ADMITTED"

        result = self.evaluate(chart, "BASELINING")
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("could not be proven", result["reasons"][0])

    def test_undeclared_edge_denied(self):
        chart = self.base_chart()
        chart["current_state"] = "DIAGNOSING"
        chart["risk_class"] = "R2"
        chart["root_cause_confidence"] = "confirmed_root_cause"

        result = self.evaluate(chart, "TREATING")
        self.assertEqual(result["decision"], "DENIED")

    def test_missing_risk_class_blocks_clinical_promotion(self):
        chart = self.base_chart()
        chart["current_state"] = "AUTHORITY_MAPPED"
        chart["policy_context"]["facts"] = {
            "authority_envelope_established": True,
        }

        result = self.evaluate(chart, "DIAGNOSING")
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("Risk class is required", result["reasons"][0])

    def test_retry_fact_is_derived_from_budget(self):
        chart = self.base_chart()
        chart["current_state"] = "SELF_TESTING"
        chart["risk_class"] = "R2"
        chart["root_cause_confidence"] = "confirmed_root_cause"
        chart["retry_budget_remaining"] = 0
        chart["policy_context"]["facts"] = {
            "retry_budget_available": True,
            "self_test_failed": True,
            "diagnosis_valid": True,
        }

        result = self.evaluate(chart, "TREATMENT_PROPOSED")
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("conflicts with derived fact retry_budget_available", result["reasons"][0])

    def test_root_cause_confidence_is_risk_derived(self):
        chart = self.base_chart()
        chart["current_state"] = "DIAGNOSING"
        chart["risk_class"] = "R3"
        chart["root_cause_confidence"] = "probable_cause"
        chart["policy_context"]["facts"] = {
            "root_cause_confidence_met": True,
            "evidence_threshold_met": True,
        }

        result = self.evaluate(chart, "DIAGNOSIS_CONFIRMED")
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("conflicts with derived fact root_cause_confidence_met", result["reasons"][0])

    def test_r2_treatment_with_current_authorization_evidence_allowed(self):
        chart = self.base_chart()
        chart["current_state"] = "TREATMENT_PROPOSED"
        chart["risk_class"] = "R2"
        chart["root_cause_confidence"] = "confirmed_root_cause"
        chart["authority"]["treatment_authorized"] = True
        chart["authority"]["operator_authorization_ref"] = "EV-AUTH-001"
        chart["evidence"]["refs"] = ["EV-DIAG-001", "EV-AUTH-001"]
        chart["policy_context"]["facts"] = {
            "authorization_scoped": True,
        }
        chart["policy_context"]["fact_evidence"] = {
            "root_cause_confidence_met": ["EV-DIAG-001"],
            "authorization_scoped": ["EV-AUTH-001"],
        }

        records = [
            evidence(
                "EV-DIAG-001",
                "diagnosis",
                "case_orchestrator",
                "pass",
            ),
            evidence(
                "EV-AUTH-001",
                "authorization",
                "authorized_operator",
                "granted",
                scope="treatment",
            ),
        ]

        result = self.evaluate(chart, "TREATING", records)
        self.assertEqual(result["decision"], "ALLOWED")

    def test_r2_treatment_cannot_manufacture_authorization_boolean(self):
        chart = self.base_chart()
        chart["current_state"] = "TREATMENT_PROPOSED"
        chart["risk_class"] = "R2"
        chart["root_cause_confidence"] = "confirmed_root_cause"
        chart["authority"]["treatment_authorized"] = True
        chart["policy_context"]["facts"] = {
            "authorization_scoped": True,
        }

        result = self.evaluate(chart, "TREATING", [])
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn(
            "treatment_authorized conflicts with current scoped authorization evidence",
            result["reasons"][0],
        )

    def test_authorization_scoped_fact_cannot_exist_without_evidence(self):
        chart = self.base_chart()
        chart["current_state"] = "TREATMENT_PROPOSED"
        chart["risk_class"] = "R2"
        chart["root_cause_confidence"] = "confirmed_root_cause"
        chart["authority"]["treatment_authorized"] = False
        chart["policy_context"]["facts"] = {
            "authorization_scoped": True,
        }

        result = self.evaluate(chart, "TREATING", [])
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn(
            "conflicts with derived fact authorization_scoped",
            result["reasons"][0],
        )

    def test_r2_authorization_fact_cannot_disable_required_authorization(self):
        chart = self.base_chart()
        chart["current_state"] = "TREATMENT_PROPOSED"
        chart["risk_class"] = "R2"
        chart["root_cause_confidence"] = "confirmed_root_cause"
        chart["policy_context"]["facts"] = {
            "explicit_authorization_required": False,
        }

        result = self.evaluate(chart, "TREATING", [])
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn(
            "conflicts with derived fact explicit_authorization_required",
            result["reasons"][0],
        )

    def test_fact_evidence_must_be_listed_in_chart_evidence_refs(self):
        chart = self.base_chart()
        chart["current_state"] = "DIAGNOSING"
        chart["risk_class"] = "R2"
        chart["root_cause_confidence"] = "confirmed_root_cause"
        chart["policy_context"]["facts"] = {
            "evidence_threshold_met": True,
        }
        chart["policy_context"]["fact_evidence"] = {
            "root_cause_confidence_met": ["EV-DIAG-001"],
            "evidence_threshold_met": ["EV-DIAG-001"],
        }

        records = [
            evidence(
                "EV-DIAG-001",
                "diagnosis",
                "case_orchestrator",
                "pass",
            )
        ]

        result = self.evaluate(chart, "DIAGNOSIS_CONFIRMED", records)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("not listed in chart evidence.refs", result["reasons"][0])

    def r3_discharge_chart(self):
        chart = self.base_chart()
        chart["current_state"] = "DISCHARGE_REVIEW"
        chart["risk_class"] = "R3"
        chart["root_cause_confidence"] = "confirmed_root_cause"
        chart["verification"]["independent"] = "pass"
        chart["verification"]["adversarial"] = "pass"
        chart["verification"]["resilience"] = "pass"
        chart["verification"]["regression"] = "pass"

        chart["policy_context"]["facts"] = {
            "required_evidence_satisfied": True,
            "blocking_residual_risk": False,
        }

        chart["policy_context"]["fact_evidence"] = {
            "root_cause_confidence_met": ["EV-DIAG-001"],
            "independent_verification_passed": ["EV-INDEP-001"],
            "adversarial_verification_passed": ["EV-ADV-001"],
            "resilience_verification_passed": ["EV-RES-001"],
            "required_evidence_satisfied": ["EV-DISCHARGE-001"],
            "blocking_residual_risk": ["EV-RISK-001"],
        }

        chart["evidence"]["refs"] = [
            "EV-DIAG-001",
            "EV-INDEP-001",
            "EV-ADV-001",
            "EV-RES-001",
            "EV-DISCHARGE-001",
            "EV-RISK-001",
            "EV-DISCHARGE-AUTH-001",
        ]

        records = [
            evidence(
                "EV-DIAG-001",
                "diagnosis",
                "case_orchestrator",
                "pass",
            ),
            evidence(
                "EV-INDEP-001",
                "independent_verification",
                "independent_verifier",
                "pass",
                fresh_context=True,
            ),
            evidence(
                "EV-ADV-001",
                "adversarial_verification",
                "adversarial_verifier",
                "pass",
            ),
            evidence(
                "EV-RES-001",
                "resilience_verification",
                "resilience_verifier",
                "pass",
            ),
            evidence(
                "EV-DISCHARGE-001",
                "discharge_review",
                "independent_verifier",
                "pass",
            ),
            evidence(
                "EV-RISK-001",
                "residual_risk_review",
                "independent_verifier",
                "pass",
            ),
            evidence(
                "EV-DISCHARGE-AUTH-001",
                "authorization",
                "authorized_operator",
                "granted",
                scope="discharge",
            ),
        ]

        return chart, records

    def test_r3_recovered_discharge_with_full_evidence_allowed(self):
        chart, records = self.r3_discharge_chart()

        result = self.evaluate(chart, "RECOVERED", records)
        self.assertEqual(result["decision"], "ALLOWED")

    def test_r3_observation_discharge_still_requires_evidence_and_authorization(self):
        chart, records = self.r3_discharge_chart()
        chart["policy_context"]["facts"]["recovery_requirements_satisfied"] = True
        chart["policy_context"]["facts"]["observation_required"] = True
        chart["policy_context"]["fact_evidence"]["recovery_requirements_satisfied"] = [
            "EV-DISCHARGE-001"
        ]
        chart["policy_context"]["fact_evidence"]["observation_required"] = [
            "EV-RISK-001"
        ]

        allowed = self.evaluate(
            chart,
            "RECOVERED_OBSERVATION_REQUIRED",
            records,
        )
        self.assertEqual(allowed["decision"], "ALLOWED")

        records_without_discharge_auth = [
            record
            for record in records
            if record["evidence_id"] != "EV-DISCHARGE-AUTH-001"
        ]
        chart["evidence"]["refs"].remove("EV-DISCHARGE-AUTH-001")

        blocked = self.evaluate(
            chart,
            "RECOVERED_OBSERVATION_REQUIRED",
            records_without_discharge_auth,
        )
        self.assertEqual(blocked["decision"], "BLOCKED")
        self.assertIn(
            "lacks explicit discharge authorization",
            blocked["reasons"][0],
        )

    def test_r3_recovered_discharge_without_discharge_authorization_blocks(self):
        chart, records = self.r3_discharge_chart()
        records = [
            record
            for record in records
            if record["evidence_id"] != "EV-DISCHARGE-AUTH-001"
        ]
        chart["evidence"]["refs"].remove("EV-DISCHARGE-AUTH-001")

        result = self.evaluate(chart, "RECOVERED", records)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("lacks explicit discharge authorization", result["reasons"][0])

    def test_r3_recovered_discharge_requires_resilience_pass(self):
        chart, records = self.r3_discharge_chart()
        chart["verification"]["resilience"] = "fail"
        chart["policy_context"]["facts"]["resilience_verification_passed"] = True

        result = self.evaluate(chart, "RECOVERED", records)
        self.assertEqual(result["decision"], "BLOCKED")

    def test_disconnected_state_history_blocks(self):
        chart = self.base_chart()
        chart["current_state"] = "DIAGNOSING"
        chart["state_history"] = [
            {
                "from": None,
                "to": "ADMITTED",
                "at": None,
                "evidence_ref": None,
                "authorization_ref": None,
            },
            {
                "from": "BASELINING",
                "to": "AUTHORITY_MAPPED",
                "at": None,
                "evidence_ref": None,
                "authorization_ref": None,
            },
            {
                "from": "AUTHORITY_MAPPED",
                "to": "DIAGNOSING",
                "at": None,
                "evidence_ref": None,
                "authorization_ref": None,
            },
        ]

        result = self.evaluate(chart, "ROOT_CAUSE_UNRESOLVED")
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("disconnected", result["reasons"][0])

    def test_terminal_case_cannot_be_promoted(self):
        chart = self.base_chart()
        chart["current_state"] = "BLOCKED"
        chart["terminal_outcome"] = "BLOCKED"

        result = self.evaluate(chart, "ADMITTED")
        self.assertEqual(result["decision"], "DENIED")

    def test_evaluation_does_not_modify_patient_chart(self):
        chart = self.base_chart()
        chart["current_state"] = "ADMITTED"
        chart["policy_context"]["facts"] = {
            "containment_required": False,
        }

        chart_path = self.write_chart(chart)
        before = chart_path.read_bytes()
        result = evaluate_case_promotion(chart_path, "BASELINING", None)
        after = chart_path.read_bytes()

        self.assertEqual(result["decision"], "ALLOWED")
        self.assertEqual(before, after)

    def test_cross_case_evidence_bundle_blocks(self):
        chart = self.base_chart()
        chart["current_state"] = "ADMITTED"
        chart["policy_context"]["facts"] = {
            "containment_required": False,
        }

        chart_path = self.write_chart(chart)
        bundle_path = self.write_bundle([], case_id="CASE-OTHER")
        result = evaluate_case_promotion(
            chart_path,
            "BASELINING",
            bundle_path,
        )

        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("Evidence bundle case_id does not match", result["reasons"][0])

    def test_evidence_record_case_mismatch_blocks(self):
        chart = self.base_chart()
        chart["current_state"] = "ADMITTED"
        chart["policy_context"]["facts"] = {
            "containment_required": False,
        }

        records = [
            evidence(
                "EV-CROSS-CASE",
                "repository_inspection",
                "external_evaluator",
                "observed",
                case_id="CASE-OTHER",
            )
        ]

        result = self.evaluate(chart, "BASELINING", records)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn(
            "Evidence case_id does not match active case",
            result["reasons"][0],
        )

    def test_tampered_evidence_integrity_blocks(self):
        chart = self.base_chart()
        chart["current_state"] = "ADMITTED"
        chart["policy_context"]["facts"] = {
            "containment_required": False,
        }

        records = [
            evidence(
                "EV-TAMPERED",
                "repository_inspection",
                "external_evaluator",
                "observed",
            )
        ]
        records[0]["integrity"]["digest"] = "sha256:" + ("0" * 64)

        result = self.evaluate(chart, "BASELINING", records)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn(
            "Evidence integrity digest mismatch",
            result["reasons"][0],
        )

    def test_bundle_identity_must_be_referenced_by_chart(self):
        chart = self.base_chart()
        chart["current_state"] = "ADMITTED"
        chart["policy_context"]["facts"] = {
            "containment_required": False,
        }

        records = [
            evidence(
                "EV-IDENTITY-REF",
                "repository_inspection",
                "external_evaluator",
                "observed",
            )
        ]

        chart_path = self.write_chart(chart)
        bundle_path = self.write_bundle(records, chart["case_id"])
        result = evaluate_case_promotion(
            chart_path,
            "BASELINING",
            bundle_path,
        )

        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn(
            "identity attestations not referenced by the patient chart",
            result["reasons"][0],
        )

    def test_evidence_wrong_producer_role_blocks(self):
        chart, records = self.r3_discharge_chart()
        for record in records:
            if record["evidence_id"] == "EV-INDEP-001":
                record["producer_role"] = "treating_agent"

        result = self.evaluate(chart, "RECOVERED", records)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn(
            "producer role does not match identity attestation",
            result["reasons"][0],
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_evidence_provenance import (  # noqa: E402
    ProvenanceFailure,
    validate_fact_provenance,
    validate_records,
)


def record(
    evidence_id,
    kind,
    role,
    result,
    *,
    fresh_context=None,
):
    item = {
        "evidence_id": evidence_id,
        "case_id": "EVAL-TEST",
        "kind": kind,
        "producer_role": role,
        "subject": "synthetic test evidence",
        "result": result,
        "synthetic": True,
        "visibility": "synthetic_public",
    }
    if fresh_context is not None:
        item["fresh_context"] = fresh_context
    return item


class EvidenceProvenanceTests(unittest.TestCase):
    def test_scoped_authorization_requires_authorization_evidence(self):
        index = validate_records(
            [
                record(
                    "EV-TEST-AUTH",
                    "authorization",
                    "authorized_operator",
                    "granted",
                )
            ],
            public_synthetic=True,
        )

        validate_fact_provenance(
            {"authorization_scoped": True},
            {"authorization_scoped": ["EV-TEST-AUTH"]},
            index,
        )

    def test_scoped_authorization_rejects_wrong_kind(self):
        index = validate_records(
            [
                record(
                    "EV-TEST-WRONG",
                    "treatment_result",
                    "treating_agent",
                    "pass",
                )
            ],
            public_synthetic=True,
        )

        with self.assertRaises(ProvenanceFailure):
            validate_fact_provenance(
                {"authorization_scoped": True},
                {"authorization_scoped": ["EV-TEST-WRONG"]},
                index,
            )

    def test_independent_pass_requires_independent_verifier_and_fresh_context(self):
        bad_role = validate_records(
            [
                record(
                    "EV-TEST-INDEP",
                    "independent_verification",
                    "treating_agent",
                    "pass",
                    fresh_context=True,
                )
            ],
            public_synthetic=True,
        )

        with self.assertRaises(ProvenanceFailure):
            validate_fact_provenance(
                {"independent_verification_passed": True},
                {"independent_verification_passed": ["EV-TEST-INDEP"]},
                bad_role,
            )

        stale = validate_records(
            [
                record(
                    "EV-TEST-INDEP-FRESH",
                    "independent_verification",
                    "independent_verifier",
                    "pass",
                    fresh_context=False,
                )
            ],
            public_synthetic=True,
        )

        with self.assertRaises(ProvenanceFailure):
            validate_fact_provenance(
                {"independent_verification_passed": True},
                {
                    "independent_verification_passed": [
                        "EV-TEST-INDEP-FRESH"
                    ]
                },
                stale,
            )

    def test_treatment_scope_requires_treatment_and_authorization(self):
        index = validate_records(
            [
                record(
                    "EV-TEST-TREAT",
                    "treatment_result",
                    "treating_agent",
                    "pass",
                )
            ],
            public_synthetic=True,
        )

        with self.assertRaises(ProvenanceFailure):
            validate_fact_provenance(
                {"treatment_within_authorized_scope": True},
                {
                    "treatment_within_authorized_scope": [
                        "EV-TEST-TREAT"
                    ]
                },
                index,
            )

    def test_unknown_evidence_reference_fails(self):
        with self.assertRaises(ProvenanceFailure):
            validate_fact_provenance(
                {"required_evidence_satisfied": True},
                {"required_evidence_satisfied": ["EV-UNKNOWN"]},
                {},
            )

    def test_duplicate_evidence_ids_fail(self):
        records = [
            record(
                "EV-DUPLICATE",
                "authorization",
                "authorized_operator",
                "granted",
            ),
            record(
                "EV-DUPLICATE",
                "authorization",
                "authorized_operator",
                "granted",
            ),
        ]

        with self.assertRaises(ProvenanceFailure):
            validate_records(records, public_synthetic=True)

    def test_expected_case_id_rejects_cross_case_evidence(self):
        item = record(
            "EV-CROSS-CASE",
            "authorization",
            "authorized_operator",
            "granted",
        )
        item["case_id"] = "EVAL-OTHER"

        with self.assertRaises(ProvenanceFailure):
            validate_records(
                [item],
                public_synthetic=True,
                expected_case_id="EVAL-TEST",
            )

    def test_public_assurance_rejects_private_visibility(self):
        item = record(
            "EV-PRIVATE",
            "authorization",
            "authorized_operator",
            "granted",
        )
        item["visibility"] = "local_private"

        with self.assertRaises(ProvenanceFailure):
            validate_records([item], public_synthetic=True)


if __name__ == "__main__":
    unittest.main()

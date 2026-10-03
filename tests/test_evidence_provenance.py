from __future__ import annotations

import hashlib
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_evidence_provenance import (  # noqa: E402
    ProvenanceFailure,
    validate_fact_provenance,
    validate_identities,
    validate_records,
)


def identity(identity_id, role, kind, session_ref=None):
    item = {
        "identity_id": identity_id,
        "identity_kind": kind,
        "role": role,
        "runtime_class": "synthetic-test-runtime",
        "observer_role": "ci_harness",
        "observed_runtime": True,
        "synthetic": True,
        "visibility": "synthetic_public",
    }
    if session_ref is not None:
        item["session_ref"] = session_ref
    return item


def evidence(
    evidence_id,
    kind,
    role,
    result,
    identity_ref,
    *,
    fresh_context=None,
):
    payload = f"{evidence_id}|{kind}|{role}|{result}"
    item = {
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
    }
    if fresh_context is not None:
        item["fresh_context"] = fresh_context
    return item


class EvidenceIntegrityAndProvenanceTests(unittest.TestCase):
    def test_valid_scoped_authorization_passes(self):
        identities = validate_identities(
            [
                identity(
                    "ID-TEST-OPERATOR",
                    "authorized_operator",
                    "human_operator",
                )
            ],
            public_synthetic=True,
        )
        records = validate_records(
            [
                evidence(
                    "EV-TEST-AUTH",
                    "authorization",
                    "authorized_operator",
                    "granted",
                    "ID-TEST-OPERATOR",
                )
            ],
            identities,
            public_synthetic=True,
        )
        validate_fact_provenance(
            {"authorization_scoped": True},
            {"authorization_scoped": ["EV-TEST-AUTH"]},
            records,
        )

    def test_digest_tampering_fails(self):
        identities = validate_identities(
            [identity("ID-TEST-OPERATOR", "authorized_operator", "human_operator")],
            public_synthetic=True,
        )
        item = evidence(
            "EV-TEST-AUTH",
            "authorization",
            "authorized_operator",
            "granted",
            "ID-TEST-OPERATOR",
        )
        item["integrity"]["digest"] = "sha256:" + ("0" * 64)

        with self.assertRaises(ProvenanceFailure):
            validate_records([item], identities, public_synthetic=True)

    def test_noncanonical_payload_fails(self):
        identities = validate_identities(
            [identity("ID-TEST-OPERATOR", "authorized_operator", "human_operator")],
            public_synthetic=True,
        )
        item = evidence(
            "EV-TEST-AUTH",
            "authorization",
            "authorized_operator",
            "granted",
            "ID-TEST-OPERATOR",
        )
        payload = "arbitrary synthetic payload"
        item["integrity"]["synthetic_payload"] = payload
        item["integrity"]["digest"] = (
            "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
        )

        with self.assertRaises(ProvenanceFailure):
            validate_records([item], identities, public_synthetic=True)

    def test_unknown_producer_identity_fails(self):
        item = evidence(
            "EV-TEST-AUTH",
            "authorization",
            "authorized_operator",
            "granted",
            "ID-UNKNOWN",
        )
        with self.assertRaises(ProvenanceFailure):
            validate_records([item], {}, public_synthetic=True)

    def test_producer_role_must_match_identity_role(self):
        identities = validate_identities(
            [
                identity(
                    "ID-TEST-TREAT",
                    "treating_agent",
                    "agent_runtime",
                    "SYN-TEST-PATIENT",
                )
            ],
            public_synthetic=True,
        )
        item = evidence(
            "EV-TEST-AUTH",
            "authorization",
            "authorized_operator",
            "granted",
            "ID-TEST-TREAT",
        )
        with self.assertRaises(ProvenanceFailure):
            validate_records([item], identities, public_synthetic=True)

    def test_identity_role_kind_mismatch_fails(self):
        item = identity(
            "ID-TEST-MISMATCH",
            "independent_verifier",
            "agent_runtime",
            "SYN-TEST-MISMATCH",
        )

        with self.assertRaises(ProvenanceFailure):
            validate_identities([item], public_synthetic=True)

    def test_independent_verification_requires_fresh_context(self):
        identities = validate_identities(
            [
                identity(
                    "ID-TEST-INDEP",
                    "independent_verifier",
                    "verifier_runtime",
                    "SYN-TEST-INDEP",
                )
            ],
            public_synthetic=True,
        )
        records = validate_records(
            [
                evidence(
                    "EV-TEST-INDEP",
                    "independent_verification",
                    "independent_verifier",
                    "pass",
                    "ID-TEST-INDEP",
                    fresh_context=False,
                )
            ],
            identities,
            public_synthetic=True,
        )

        with self.assertRaises(ProvenanceFailure):
            validate_fact_provenance(
                {"independent_verification_passed": True},
                {"independent_verification_passed": ["EV-TEST-INDEP"]},
                records,
            )

    def test_public_identity_rejects_private_visibility(self):
        item = identity(
            "ID-TEST-INDEP",
            "independent_verifier",
            "verifier_runtime",
            "SYN-TEST-INDEP",
        )
        item["visibility"] = "local_private"

        with self.assertRaises(ProvenanceFailure):
            validate_identities([item], public_synthetic=True)

    def test_duplicate_identity_ids_fail(self):
        item = identity(
            "ID-DUPLICATE",
            "independent_verifier",
            "verifier_runtime",
            "SYN-DUPLICATE",
        )
        with self.assertRaises(ProvenanceFailure):
            validate_identities([item, dict(item)], public_synthetic=True)


if __name__ == "__main__":
    unittest.main()

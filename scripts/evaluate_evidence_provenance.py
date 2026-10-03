#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]


class ProvenanceFailure(Exception):
    pass


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str):
    if not condition:
        raise ProvenanceFailure(message)


def sha256_text(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def validate_identities(identities: list[dict], public_synthetic: bool = False):
    schema = load_json(ROOT / "identity" / "identity-attestation.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)

    index = {}
    for identity in identities:
        jsonschema.validate(instance=identity, schema=schema)
        identity_id = identity["identity_id"]
        require(identity_id not in index, f"Duplicate identity ID: {identity_id}")

        if public_synthetic:
            require(
                identity["synthetic"] is True,
                f"Public assurance identity is not synthetic: {identity_id}",
            )
            require(
                identity["visibility"] == "synthetic_public",
                f"Public assurance identity has invalid visibility: {identity_id}",
            )

        index[identity_id] = identity

    return index


def validate_integrity(record: dict, public_synthetic: bool = False):
    integrity = record["integrity"]
    payload = integrity.get("synthetic_payload")

    if payload is not None:
        require(
            sha256_text(payload) == integrity["digest"],
            f"Evidence integrity digest mismatch: {record['evidence_id']}",
        )

    if public_synthetic:
        require(
            integrity["scope"] == "synthetic_payload",
            f"Public synthetic evidence has invalid integrity scope: {record['evidence_id']}",
        )
        require(
            payload is not None,
            f"Public synthetic evidence lacks synthetic integrity payload: {record['evidence_id']}",
        )


def validate_records(
    records: list[dict],
    identity_index: dict,
    public_synthetic: bool = False,
):
    schema = load_json(ROOT / "evidence" / "evidence-record.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)

    index = {}
    for record in records:
        jsonschema.validate(instance=record, schema=schema)
        evidence_id = record["evidence_id"]
        require(evidence_id not in index, f"Duplicate evidence ID: {evidence_id}")

        identity_id = record["producer_identity_ref"]
        require(
            identity_id in identity_index,
            f"Evidence references unknown producer identity: {evidence_id}",
        )
        require(
            identity_index[identity_id]["role"] == record["producer_role"],
            f"Evidence producer role does not match identity attestation: {evidence_id}",
        )

        validate_integrity(record, public_synthetic=public_synthetic)

        if public_synthetic:
            require(
                record["synthetic"] is True,
                f"Public assurance evidence is not synthetic: {evidence_id}",
            )
            require(
                record["visibility"] == "synthetic_public",
                f"Public assurance evidence has invalid visibility: {evidence_id}",
            )

        index[evidence_id] = record

    return index


def validate_fact_provenance(
    facts: dict,
    fact_evidence: dict,
    evidence_index: dict,
):
    policy = load_json(ROOT / "evidence" / "fact-provenance.json")
    policy_schema = load_json(ROOT / "evidence" / "fact-provenance.schema.json")
    jsonschema.Draft202012Validator.check_schema(policy_schema)
    jsonschema.validate(instance=policy, schema=policy_schema)

    for fact, value in facts.items():
        rule = policy["fact_rules"].get(fact)
        if not rule or value is not rule["applies_when"]:
            continue

        refs = fact_evidence.get(fact, [])
        require(refs, f"High-impact fact lacks evidence references: {fact}")

        records = []
        for evidence_id in refs:
            require(
                evidence_id in evidence_index,
                f"Unknown evidence reference for {fact}: {evidence_id}",
            )
            records.append(evidence_index[evidence_id])

        for requirement in rule["requirements"]:
            matches = [
                record
                for record in records
                if record["kind"] == requirement["kind"]
                and record["producer_role"] in requirement["producer_roles"]
                and record["result"] in requirement["results"]
                and (
                    not requirement.get("requires_fresh_context", False)
                    or record.get("fresh_context") is True
                )
            ]

            require(
                len(matches) >= requirement["min_count"],
                f"Evidence provenance requirement not satisfied for {fact}: {requirement['kind']}",
            )


def validate_event_evidence(event: dict, evidence_index: dict, identity_index: dict):
    event_type = event["type"]

    if event_type == "authorization" and event.get("status") == "granted":
        evidence_id = event.get("evidence_ref")
        require(evidence_id, "Granted authorization event lacks evidence_ref.")
        require(
            evidence_id in evidence_index,
            f"Unknown authorization evidence reference: {evidence_id}",
        )

        record = evidence_index[evidence_id]
        require(record["kind"] == "authorization", "Authorization event evidence has wrong kind.")
        require(record["result"] == "granted", "Authorization event evidence is not granted.")
        require(
            record["producer_role"] in {"authorized_operator", "platform_authority"},
            "Authorization event evidence has invalid producer role.",
        )

    if event_type == "verification" and event.get("status") == "pass":
        mode = event.get("mode")
        expected = {
            "independent": ("independent_verification", {"independent_verifier"}),
            "adversarial": (
                "adversarial_verification",
                {"adversarial_verifier", "ci_harness"},
            ),
            "resilience": (
                "resilience_verification",
                {"resilience_verifier", "ci_harness"},
            ),
            "regression": (
                "regression_review",
                {"independent_verifier", "ci_harness", "external_evaluator"},
            ),
        }

        require(mode in expected, "Unknown verification mode for evidence provenance.")
        evidence_id = event.get("evidence_ref")
        require(evidence_id, f"{mode} verification PASS lacks evidence_ref.")
        require(
            evidence_id in evidence_index,
            f"Unknown verification evidence reference: {evidence_id}",
        )

        record = evidence_index[evidence_id]
        kind, roles = expected[mode]
        require(record["kind"] == kind, f"{mode} verification evidence has wrong kind.")
        require(
            record["producer_role"] in roles,
            f"{mode} verification evidence has invalid producer role.",
        )
        require(record["result"] == "pass", f"{mode} verification evidence is not PASS.")

        identity_ref = event.get("verifier_identity_ref")
        require(identity_ref, f"{mode} verification PASS lacks verifier_identity_ref.")
        require(
            identity_ref in identity_index,
            f"{mode} verification references unknown verifier identity.",
        )
        require(
            identity_ref == record["producer_identity_ref"],
            f"{mode} verification identity does not match evidence producer identity.",
        )

        if mode == "independent":
            require(
                record.get("fresh_context") is True,
                "Independent verification evidence lacks fresh context.",
            )

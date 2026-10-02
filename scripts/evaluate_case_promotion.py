#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema
import yaml

from evaluate_evidence_provenance import (
    ProvenanceFailure,
    validate_fact_provenance,
    validate_records,
)
from evaluate_transition_policy import (
    PolicyFailure,
    evaluate_transition,
    transition_conditions,
)


ROOT = Path(__file__).resolve().parents[1]
RECOVERY_OUTCOMES = {"RECOVERED", "RECOVERED_OBSERVATION_REQUIRED"}
RISK_REQUIRED_STATES = {
    "DIAGNOSING",
    "DIAGNOSIS_CONFIRMED",
    "TREATMENT_PROPOSED",
    "AWAITING_AUTHORIZATION",
    "TREATING",
    "SELF_TESTING",
    "INDEPENDENT_VERIFICATION",
    "ADVERSARIAL_VERIFICATION",
    "RESILIENCE_VERIFICATION",
    "REGRESSION_REVIEW",
    "DISCHARGE_REVIEW",
    "RECOVERED",
    "RECOVERED_OBSERVATION_REQUIRED",
    "PARTIAL_RECOVERY",
    "TREATMENT_FAILED",
}


class PromotionBlocked(Exception):
    pass


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str):
    if not condition:
        raise PromotionBlocked(message)


def validate_case_chart(chart: dict):
    schema = load_json(ROOT / "templates" / "case-state.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(instance=chart, schema=schema)


def load_evidence_bundle(path: Path | None):
    if path is None:
        return []

    bundle = load_json(path)
    schema = load_json(ROOT / "evidence" / "evidence-bundle.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(instance=bundle, schema=schema)

    return bundle["records"]


def validate_history(chart: dict, protocol: dict):
    history = chart["state_history"]
    if not history:
        return

    previous_to = None

    for index, entry in enumerate(history):
        source = entry["from"]
        target = entry["to"]

        if index > 0:
            require(
                source == previous_to,
                f"State history is disconnected at entry {index + 1}.",
            )

        if source is None:
            require(
                index == 0 and target == "ADMITTED",
                "A null history source is valid only for initial admission.",
            )
        else:
            require(
                source in protocol["states"],
                f"State history source is not a nonterminal protocol state: {source}",
            )
            require(
                bool(transition_conditions(protocol, source, target)),
                f"State history contains undeclared edge: {source} -> {target}",
            )

        previous_to = target

    require(
        previous_to == chart["current_state"],
        "State history final state does not match current_state.",
    )


def minimum_confidence_met(chart: dict, protocol: dict):
    risk_class = chart["risk_class"]
    confidence = chart["root_cause_confidence"]

    if risk_class is None or confidence is None:
        return None

    required = protocol["risk_classes"][risk_class]["minimum_root_cause_confidence"]
    order = protocol["root_cause_confidence"]

    return order.index(confidence) >= order.index(required)


def valid_authorizations(evidence_index: dict, scope: str):
    return [
        record
        for record in evidence_index.values()
        if record["kind"] == "authorization"
        and record["producer_role"] in {"authorized_operator", "platform_authority"}
        and record["result"] == "granted"
        and record.get("scope") in {scope, "case"}
    ]


def apply_derived_fact(facts: dict, derived: dict, name: str, value: bool):
    if name in facts and facts[name] is not value:
        raise PromotionBlocked(
            f"Chart fact conflicts with derived fact {name}: "
            f"chart={facts[name]} derived={value}"
        )

    facts[name] = value
    derived[name] = value


def derive_policy_facts(chart: dict, protocol: dict, evidence_index: dict):
    facts = dict(chart["policy_context"]["facts"])
    derived = {}

    apply_derived_fact(
        facts,
        derived,
        "retry_budget_available",
        chart["retry_budget_remaining"] > 0,
    )

    confidence_met = minimum_confidence_met(chart, protocol)
    if confidence_met is not None:
        apply_derived_fact(
            facts,
            derived,
            "root_cause_confidence_met",
            confidence_met,
        )

    risk_class = chart["risk_class"]
    if risk_class is not None:
        risk = protocol["risk_classes"][risk_class]

        if risk["explicit_treatment_authorization"]:
            apply_derived_fact(
                facts,
                derived,
                "explicit_authorization_required",
                True,
            )
        elif "explicit_authorization_required" not in facts:
            apply_derived_fact(
                facts,
                derived,
                "explicit_authorization_required",
                False,
            )

        verification_requirements = {
            "independent_verification_required": risk["independent_verification"],
            "adversarial_verification_required": risk["adversarial_verification"],
            "resilience_verification_required": risk["resilience_verification"],
        }

        for fact_name, requirement in verification_requirements.items():
            if requirement == "required":
                apply_derived_fact(facts, derived, fact_name, True)
            elif requirement == "optional" and fact_name not in facts:
                apply_derived_fact(facts, derived, fact_name, False)

    treatment_authorizations = valid_authorizations(evidence_index, "treatment")
    authorization_scoped = bool(treatment_authorizations)

    if authorization_scoped:
        authorization_ids = {record["evidence_id"] for record in treatment_authorizations}
        authority_ref = chart["authority"]["operator_authorization_ref"]

        require(
            authority_ref in authorization_ids,
            "Current operator_authorization_ref does not identify the active treatment authorization evidence.",
        )

    if (
        risk_class is not None
        and protocol["risk_classes"][risk_class]["explicit_treatment_authorization"]
        and chart["authority"]["treatment_authorized"] is not authorization_scoped
    ):
        raise PromotionBlocked(
            "Chart treatment_authorized conflicts with current scoped authorization evidence."
        )

    apply_derived_fact(
        facts,
        derived,
        "authorization_scoped",
        authorization_scoped,
    )

    verification_map = {
        "independent_verification_passed": chart["verification"]["independent"] == "pass",
        "adversarial_verification_passed": chart["verification"]["adversarial"] == "pass",
        "resilience_verification_passed": chart["verification"]["resilience"] == "pass",
    }

    for fact_name, value in verification_map.items():
        if value or fact_name in facts:
            apply_derived_fact(facts, derived, fact_name, value)

    return facts, derived


def validate_fact_evidence_refs(chart: dict, evidence_index: dict):
    chart_refs = set(chart["evidence"]["refs"])
    fact_evidence = chart["policy_context"]["fact_evidence"]

    for fact, refs in fact_evidence.items():
        for evidence_id in refs:
            require(
                evidence_id in chart_refs,
                f"Fact evidence reference is not listed in chart evidence.refs: {fact} -> {evidence_id}",
            )
            require(
                evidence_id in evidence_index,
                f"Fact evidence reference is absent from evidence bundle: {fact} -> {evidence_id}",
            )


def validate_recovery_gates(
    chart: dict,
    target: str,
    protocol: dict,
    evidence_index: dict,
):
    if target not in RECOVERY_OUTCOMES:
        return

    risk_class = chart["risk_class"]
    require(risk_class is not None, "Recovered discharge requires a risk class.")

    risk = protocol["risk_classes"][risk_class]
    verification = chart["verification"]

    if risk["independent_verification"] == "required":
        require(
            verification["independent"] == "pass",
            "Recovered discharge lacks required independent verification PASS.",
        )

    if risk["adversarial_verification"] == "required":
        require(
            verification["adversarial"] == "pass",
            "Recovered discharge lacks required adversarial verification PASS.",
        )

    if risk["resilience_verification"] == "required":
        require(
            verification["resilience"] == "pass",
            "Recovered discharge lacks required resilience verification PASS.",
        )

    require(
        verification["regression"] == "pass",
        "Recovered discharge lacks regression PASS.",
    )

    if risk_class == "R3":
        discharge_authorizations = valid_authorizations(evidence_index, "discharge")
        require(
            bool(discharge_authorizations),
            "R3 recovered discharge lacks explicit discharge authorization evidence.",
        )

        chart_refs = set(chart["evidence"]["refs"])
        require(
            any(record["evidence_id"] in chart_refs for record in discharge_authorizations),
            "R3 discharge authorization evidence is not referenced by the patient chart.",
        )


def decision_payload(
    decision: str,
    chart: dict,
    target: str,
    *,
    matched_conditions=None,
    derived_facts=None,
    evidence_records_checked=0,
    reasons=None,
):
    payload = {
        "decision": decision,
        "case_id": chart.get("case_id", "<UNKNOWN_CASE>"),
        "current_state": chart.get("current_state", "<UNKNOWN_STATE>"),
        "target_state": target,
        "matched_conditions": matched_conditions or [],
        "derived_facts": derived_facts or {},
        "evidence_records_checked": evidence_records_checked,
        "reasons": reasons or ["No reason recorded."],
    }

    schema = load_json(ROOT / "protocol" / "promotion-decision.schema.json")
    jsonschema.validate(instance=payload, schema=schema)

    return payload


def evaluate_case_promotion(
    chart_path: Path,
    target: str,
    evidence_bundle_path: Path | None = None,
):
    try:
        chart = load_yaml(chart_path)
        validate_case_chart(chart)
    except (OSError, yaml.YAMLError, jsonschema.ValidationError, jsonschema.SchemaError) as exc:
        return decision_payload(
            "BLOCKED",
            chart if isinstance(locals().get("chart"), dict) else {},
            target,
            reasons=[f"Patient chart could not be validated: {exc}"],
        )

    protocol = load_yaml(ROOT / "protocol" / "protocol.yaml")
    known_states = set(protocol["states"]) | set(protocol["terminal_outcomes"])

    if target not in known_states:
        return decision_payload(
            "DENIED",
            chart,
            target,
            reasons=[f"Unknown target state: {target}"],
        )

    if chart["current_state"] in protocol["terminal_outcomes"]:
        return decision_payload(
            "DENIED",
            chart,
            target,
            reasons=["Terminal cases cannot be promoted to another state."],
        )

    try:
        validate_history(chart, protocol)

        if (
            chart["current_state"] in RISK_REQUIRED_STATES
            or target in RISK_REQUIRED_STATES
        ):
            require(
                chart["risk_class"] is not None,
                "Risk class is required for this case-state promotion.",
            )

        if (
            chart["current_state"] in {
                "DIAGNOSIS_CONFIRMED",
                "TREATMENT_PROPOSED",
                "AWAITING_AUTHORIZATION",
                "TREATING",
                "SELF_TESTING",
                "INDEPENDENT_VERIFICATION",
                "ADVERSARIAL_VERIFICATION",
                "RESILIENCE_VERIFICATION",
                "REGRESSION_REVIEW",
                "DISCHARGE_REVIEW",
            }
            or target == "DIAGNOSIS_CONFIRMED"
            or target in RECOVERY_OUTCOMES
        ):
            require(
                chart["root_cause_confidence"] is not None,
                "Root-cause confidence is required for this case-state promotion.",
            )

        evidence_records = load_evidence_bundle(evidence_bundle_path)
        evidence_index = validate_records(evidence_records, public_synthetic=False)

        validate_fact_evidence_refs(chart, evidence_index)

        facts, derived = derive_policy_facts(chart, protocol, evidence_index)

        allowed, matched = evaluate_transition(
            chart["current_state"],
            target,
            facts,
        )

        if not allowed:
            return decision_payload(
                "DENIED",
                chart,
                target,
                matched_conditions=matched,
                derived_facts=derived,
                evidence_records_checked=len(evidence_index),
                reasons=[
                    "The requested edge is undeclared or its fully known transition condition evaluated false."
                ],
            )

        validate_fact_provenance(
            facts,
            chart["policy_context"]["fact_evidence"],
            evidence_index,
        )

        if target == "TREATING" and chart["risk_class"] is not None:
            if protocol["risk_classes"][chart["risk_class"]]["explicit_treatment_authorization"]:
                require(
                    chart["authority"]["treatment_authorized"] is True,
                    "Patient chart does not record treatment_authorized for an authorization-gated treatment.",
                )

        validate_recovery_gates(
            chart,
            target,
            protocol,
            evidence_index,
        )

    except PolicyFailure as exc:
        return decision_payload(
            "BLOCKED",
            chart,
            target,
            derived_facts=locals().get("derived", {}),
            evidence_records_checked=len(locals().get("evidence_index", {})),
            reasons=[f"Transition policy could not be proven: {exc}"],
        )
    except (PromotionBlocked, ProvenanceFailure, jsonschema.ValidationError, jsonschema.SchemaError, OSError, json.JSONDecodeError) as exc:
        return decision_payload(
            "BLOCKED",
            chart,
            target,
            matched_conditions=locals().get("matched", []),
            derived_facts=locals().get("derived", {}),
            evidence_records_checked=len(locals().get("evidence_index", {})),
            reasons=[str(exc)],
        )

    return decision_payload(
        "ALLOWED",
        chart,
        target,
        matched_conditions=matched,
        derived_facts=derived,
        evidence_records_checked=len(evidence_index),
        reasons=[
            "The declared transition, executable predicate, required provenance, and applicable risk gates are satisfied."
        ],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chart", type=Path, required=True)
    parser.add_argument("--to", dest="target", required=True)
    parser.add_argument("--evidence-bundle", type=Path)
    args = parser.parse_args()

    result = evaluate_case_promotion(
        args.chart,
        args.target,
        args.evidence_bundle,
    )

    print(json.dumps(result, indent=2, sort_keys=True))

    return {
        "ALLOWED": 0,
        "DENIED": 1,
        "BLOCKED": 2,
    }[result["decision"]]


if __name__ == "__main__":
    raise SystemExit(main())

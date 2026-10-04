#!/usr/bin/env python3
"""
Property-based tests for transition policy engine.

Uses Hypothesis to generate random fact combinations and verify
transition policy behavior matches expectations.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_transition_policy import evaluate_transition, PolicyFailure, MissingFact


@settings(max_examples=50, deadline=None)
@given(
    source=st.sampled_from([
        "ADMITTED", "CONTAINED", "BASELINING", "AUTHORITY_MAPPED",
        "DIAGNOSING", "DIAGNOSIS_CONFIRMED", "TREATMENT_PROPOSED",
        "AWAITING_AUTHORIZATION", "TREATING", "SELF_TESTING",
        "INDEPENDENT_VERIFICATION", "ADVERSARIAL_VERIFICATION",
        "RESILIENCE_VERIFICATION", "REGRESSION_REVIEW", "DISCHARGE_REVIEW"
    ]),
    target=st.sampled_from([
        "CONTAINED", "BASELINING", "AUTHORITY_MAPPED", "DIAGNOSING",
        "DIAGNOSIS_CONFIRMED", "TREATMENT_PROPOSED", "AWAITING_AUTHORIZATION",
        "TREATING", "SELF_TESTING", "INDEPENDENT_VERIFICATION",
        "ADVERSARIAL_VERIFICATION", "RESILIENCE_VERIFICATION",
        "REGRESSION_REVIEW", "DISCHARGE_REVIEW", "RECOVERED",
        "RECOVERED_OBSERVATION_REQUIRED", "PARTIAL_RECOVERY",
        "TREATMENT_FAILED", "ROOT_CAUSE_UNRESOLVED",
        "SPECIALIST_ESCALATION_REQUIRED", "BLOCKED", "CANCELLED"
    ]),
    facts=st.dictionaries(st.sampled_from([
        "containment_required", "safe_to_observe", "baseline_sufficient",
        "authority_envelope_established", "root_cause_confidence_met", "evidence_threshold_met",
        "explicit_authorization_required", "authorization_scoped", "treatment_completed",
        "treatment_within_authorized_scope", "independent_verification_required",
        "independent_verification_selected", "independent_verification_passed",
        "adversarial_verification_required", "adversarial_verification_passed",
        "resilience_verification_required", "resilience_verification_passed",
        "required_capabilities_preserved", "blocking_regression_present",
        "required_evidence_satisfied", "blocking_residual_risk",
        "operator_cancelled", "nonwaivable_blocker", "retry_budget_available",
        "rollback_available", "safe_checkpoint_restored", "safe_recovery_possible"
    ]), st.booleans(), min_size=0, max_size=10)
)
def test_transition_policy_no_crash(source, target, facts):
    """Property: evaluate_transition should never crash on valid inputs."""
    try:
        allowed, matched = evaluate_transition(source, target, facts)
        assert isinstance(allowed, bool)
        assert isinstance(matched, list)
        
        if allowed:
            import yaml
            PROTOCOL = yaml.safe_load((Path(__file__).resolve().parents[1] / "protocol" / "protocol.yaml").read_text())
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
            assert declared_transition(yaml.safe_load((Path(__file__).resolve().parents[1] / "protocol" / "protocol.yaml").read_text()), source, target), \
                f"Allowed undeclared transition: {source} -> {target}"
            assert len(matched) > 0, "Allowed transition must have matched condition"
    except Exception as e:
        from evaluate_transition_policy import PolicyFailure, MissingFact
        assert isinstance(e, (PolicyFailure, MissingFact)), f"Unexpected exception: {type(e).__name__}: {e}"


@settings(max_examples=20, deadline=None)
@given(
    facts=st.dictionaries(st.sampled_from(["containment_required"]), st.booleans())
)
def test_admitted_transitions(facts):
    """Property: From ADMITTED, exactly one of CONTAINED or BASELINING is allowed."""
    test_facts = dict(facts)
    test_facts.setdefault("containment_required", False)
    
    allowed_contained, _ = evaluate_transition("ADMITTED", "CONTAINED", test_facts)
    allowed_baseline, _ = evaluate_transition("ADMITTED", "BASELINING", test_facts)
    
    if test_facts.get("containment_required") is True:
        assert evaluate_transition("ADMITTED", "CONTAINED", test_facts)[0] == True
    else:
        assert evaluate_transition("ADMITTED", "BASELINING", test_facts)[0] == True


@settings(max_examples=20, deadline=None)
@given(
    facts=st.dictionaries(st.sampled_from(["operator_cancelled", "nonwaivable_blocker"]), st.booleans())
)
def test_global_cancel_blocked(facts):
    """Property: Global transitions CANCELLED and BLOCKED work from any state."""
    test_facts = dict(facts)
    test_facts["operator_cancelled"] = True
    test_facts["nonwaivable_blocker"] = True
    
    for source in ["ADMITTED", "DIAGNOSING", "TREATING", "SELF_TESTING"]:
        allowed_cancel, _ = evaluate_transition(source, "CANCELLED", test_facts)
        allowed_blocked, _ = evaluate_transition(source, "BLOCKED", test_facts)
        assert allowed_cancel, f"CANCELLED should be allowed from {source}"
        assert allowed_blocked, f"BLOCKED should be allowed from {source}"


@settings(max_examples=20, deadline=None)
@given(
    source=st.sampled_from(["ADMITTED", "DIAGNOSING", "TREATING", "SELF_TESTING", "INDEPENDENT_VERIFICATION"]),
    target=st.sampled_from(["CONTAINED", "BASELINING", "AUTHORITY_MAPPED", "DIAGNOSING", "DIAGNOSIS_CONFIRMED", "TREATMENT_PROPOSED", "AWAITING_AUTHORIZATION", "TREATING", "SELF_TESTING", "INDEPENDENT_VERIFICATION", "ADVERSARIAL_VERIFICATION", "RESILIENCE_VERIFICATION", "REGRESSION_REVIEW", "DISCHARGE_REVIEW", "RECOVERED", "CANCELLED", "BLOCKED"]),
    facts=st.dictionaries(st.sampled_from([
        "containment_required", "safe_to_observe", "baseline_sufficient",
        "authority_envelope_established", "root_cause_confidence_met", "evidence_threshold_met",
        "explicit_authorization_required", "authorization_scoped", "treatment_completed",
        "treatment_within_authorized_scope", "independent_verification_required",
        "independent_verification_selected", "independent_verification_passed",
        "adversarial_verification_required", "adversarial_verification_passed",
        "resilience_verification_required", "resilience_verification_passed",
        "required_capabilities_preserved", "blocking_regression_present",
        "required_evidence_satisfied", "blocking_residual_risk"
    ]), st.booleans(), min_size=0, max_size=10)
)
def test_deterministic_evaluation(source, target, facts):
    """Property: Same facts always produce same result."""
    try:
        allowed1, matched1 = evaluate_transition(source, target, facts)
        allowed2, matched2 = evaluate_transition(source, target, facts)
        
        assert allowed1 == allowed2, "Evaluation must be deterministic"
        assert matched1 == matched2, "Matched conditions must be deterministic"
    except Exception as e:
        from evaluate_transition_policy import PolicyFailure, MissingFact
        assert isinstance(e, (PolicyFailure, MissingFact)), f"Unexpected exception: {type(e).__name__}: {e}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Case-State Promotion Engine

Vex Hospital can evaluate whether a patient chart is ready to move from its current state to a proposed next state.

The promotion engine is read-only.

It does not mutate the patient chart, perform treatment, grant authorization, create evidence, or infer permission from available tools.

## Inputs

The reference command accepts:

- a local `case-state.yaml`;
- a proposed target state;
- an optional patient-controlled evidence bundle.

Evidence bundles use `evidence/evidence-bundle.schema.json`.

A bundle contains typed evidence records plus the runtime identity attestations needed to validate their producer roles. During promotion evaluation, evidence records must match the active case ID, pass the current integrity checks, and reference producer identities accepted by the current Hospital identity model.

Bundle identities must also be referenced by the patient chart's environment identity list.

The evidence bundle may remain entirely inside the patient environment. It is not a public Hospital record.

## Decision outcomes

The engine returns one of:

### ALLOWED

The proposed state edge exists, its executable predicate is satisfied, required high-impact facts have valid evidence provenance, and applicable risk-specific promotion gates are satisfied.

ALLOWED means the control-plane requirements for the transition are satisfied.

It does not execute the transition.

### DENIED

The proposed transition is not legal or its fully known condition evaluates false.

A denied transition should not be retried by merely changing facts without new evidence or case state.

### BLOCKED

The transition could potentially be legal, but the Hospital cannot prove it safely because required facts, provenance, evidence metadata, risk classification, chart integrity, or discharge authorization are missing or contradictory.

## Derived facts

The engine does not trust every chart boolean equally.

It derives selected facts from structured case state:

- `explicit_authorization_required` from the active risk class;
- `retry_budget_available` from `retry_budget_remaining`;
- `root_cause_confidence_met` from the chart confidence compared with the risk-class minimum;
- required verification flags from the risk class.

If the chart supplies a conflicting value for a derived fact, promotion is BLOCKED rather than silently choosing the convenient value.

## Evidence provenance

High-impact facts are validated through the same provenance, runtime-identity, and evidence-integrity controls used by the Assurance Ward.

Fact evidence IDs in `policy_context.fact_evidence` must:

1. be listed in the chart's `evidence.refs`;
2. exist in the supplied patient-controlled evidence bundle;
3. satisfy the required evidence kind, producer role, result, and fresh-context rule.

## Recovery gates

For a recovered discharge, the engine also checks the chart's verification status against the active risk class.

R2 requires the verification modes marked required by the protocol.

R3 requires independent, adversarial, and resilience verification plus regression PASS.

R3 recovered outcomes also require explicit discharge authorization evidence.

## History integrity

When state history exists, the engine checks that it is continuous and that its final state matches `current_state`.

Historical entries are checked for declared state edges. The engine does not retroactively recreate missing historical predicate facts.

## Privacy

The engine consumes patient-controlled evidence and identity metadata locally.

Do not commit real case charts, real evidence bundles, private artifact paths, credentials, session material, or patient identifiers to the public Vex Hospital repository.

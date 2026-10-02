# Executable Transition Conditions

The Vex Hospital protocol uses named `when:` predicates for every legal state transition.

V1.1B gives those predicates a machine-executable reference implementation.

## Files

- `protocol/conditions.json` defines the condition registry.
- `protocol/conditions.schema.json` defines the registry contract.
- `scripts/evaluate_transition_policy.py` evaluates a proposed transition against case facts.
- `protocol/protocol.yaml` references the condition registry.

## Condition model

Conditions are built from boolean facts using:

- `fact` with an expected boolean value;
- `all` for conjunction;
- `any` for alternatives;
- `not` for negation.

The registry must exactly match every `when:` predicate used by the protocol. Unused or missing predicates fail validation.

## Fail-closed behavior

A transition is allowed only when:

1. the source and target form a declared protocol transition or applicable global transition;
2. at least one declared condition for that route evaluates true;
3. every fact required by the successful condition is present and boolean.

An undeclared transition is denied.

A missing fact cannot be interpreted as true.

A malformed fact cannot be interpreted as true.

If several conditions can lead to the same target, any fully proven condition may authorize the state transition.

## Fact provenance

The policy engine evaluates facts. It does not create them.

Facts should be derived from:

- observed patient state;
- validated evidence;
- protocol risk requirements;
- explicit authorization state;
- verified treatment or examination results;
- other patient-chart fields whose provenance is established.

A patient must not invent a fact merely because a true value would permit the next state.

Examples:

- `authorization_scoped: true` requires actual scoped authorization evidence.
- `independent_verification_passed: true` requires a valid independent verification result.
- `required_evidence_satisfied: true` requires the discharge evidence package to satisfy its contract.
- `blocking_residual_risk: false` requires an actual residual-risk review.

## Behavioral assurance

Canonical behavioral traces record `condition_facts` on every executed state transition.

The behavioral evaluator sends those facts through the same transition policy engine.

This means a trace fails when:

- the edge is undeclared;
- the path is disconnected;
- the transition predicate evaluates false;
- a required fact is missing;
- a fact is not boolean.

## Assurance boundary

Executable predicates reduce ambiguity in state promotion, but they do not make evidence automatically trustworthy.

Fact derivation and evidence provenance remain separate assurance concerns. Future runtime integrations may compute some facts directly from structured patient charts, authorization artifacts, verifier attestations, and tool/runtime telemetry.

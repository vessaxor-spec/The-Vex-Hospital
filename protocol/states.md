# Protocol States

`protocol.yaml` is the machine-readable authority for legal Vex Hospital transitions. This document explains the intended semantics.

## State groups

### Intake and evidence preservation
- **ADMITTED** — case registered; no diagnosis implied.
- **CONTAINED** — ongoing risk reduced without destroying useful evidence or capability. If containment itself changes state, it must be an authorized, least-disruptive safety action within the existing authority envelope.
- **BASELINING** — symptoms, expected behavior, variability, environment, and reproduction evidence established.
- **AUTHORITY_MAPPED** — effective identities, permissions, tools, side effects, and escalation ceiling established.

### Diagnosis
- **DIAGNOSING** — competing hypotheses are tested against evidence.
- **DIAGNOSIS_CONFIRMED** — evidence reaches the case's required root-cause confidence and evidence threshold.

### Treatment design and authorization
- **TREATMENT_PROPOSED** — bounded change, expected effect, blast radius, checkpoint, rollback, and promotion evidence are defined.
- **AWAITING_AUTHORIZATION** — consequential treatment is blocked until the required authorization exists.

### Treatment and verification
- **TREATING** — the normal treatment mutation state. Mutation must remain inside the authorized scope. Containment is the only other state that may permit narrowly bounded state change, solely for authorized risk reduction.
- **SELF_TESTING** — the treating agent checks the treatment and preserved capabilities.
- **INDEPENDENT_VERIFICATION** — a fresh verifier evaluates scoped evidence without relying on the treating agent's conclusion.
- **ADVERSARIAL_VERIFICATION** — hostile, malformed, missing, forged, contradictory, or boundary conditions are tested.
- **RESILIENCE_VERIFICATION** — dependency and environmental failures are introduced or simulated where required.
- **REGRESSION_REVIEW** — expected capabilities and unrelated critical behavior are checked for degradation.
- **DISCHARGE_REVIEW** — the complete evidence package and residual risk are assessed.

## Terminal outcomes

- **RECOVERED**
- **RECOVERED_OBSERVATION_REQUIRED**
- **PARTIAL_RECOVERY**
- **TREATMENT_FAILED**
- **ROOT_CAUSE_UNRESOLVED**
- **SPECIALIST_ESCALATION_REQUIRED**
- **BLOCKED**
- **CANCELLED**

A terminal outcome is a scoped case result, not a universal safety judgment. An authorized operator may cancel any nonterminal case, and a non-waivable safety or authority condition may fail closed to BLOCKED from any nonterminal state.

## Transition discipline

- Unlisted transitions are forbidden.
- Evidence can raise risk at any time.
- Risk must not silently decrease merely to satisfy a gate.
- If new evidence invalidates an earlier assumption, return to the earliest affected state.
- A failed treatment or verification step may return to treatment planning only when the diagnosis remains valid, a safe checkpoint or recovery state has been restored, and an explicit retry budget remains.
- The default retry budget is zero. Each retry requires a new treatment plan.
- R3 retries require fresh operator authorization for every retry.
- Do not repeatedly patch a failing treatment without revisiting diagnosis when the evidence has changed.
- A required verification stage cannot be bypassed because the treating agent is confident.

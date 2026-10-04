# Vex Hospital Clinical Handbook

This handbook explains how a checked-in AI patient moves from symptoms to diagnosis, treatment, recovery testing, and discharge.

The machine-readable protocol controls legal state transitions. This handbook explains the clinical work performed inside those states. The protocol is defined in `protocol/protocol.yaml`.

## Clinical pathway

**Check-in → Triage → Examination → Differential Diagnosis → Root-Cause Confirmation → Treatment Plan → Authorization → Treatment → Recovery Testing → Independent Examination → Discharge Review → Follow-up**

This pathway maps to the protocol states defined in `protocol/protocol.yaml`:
ADMITTED → CONTAINED → BASELINING → AUTHORITY_MAPPED → DIAGNOSING → DIAGNOSIS_CONFIRMED → TREATMENT_PROPOSED → AWAITING_AUTHORIZATION → TREATING → SELF_TESTING → INDEPENDENT_VERIFICATION → ADVERSARIAL_VERIFICATION → RESILIENCE_VERIFICATION → REGRESSION_REVIEW → DISCHARGE_REVIEW → Terminal Outcome

## Clinical rule

**Specialists are uncertainty reducers, not idea generators.**

Do not send every patient to every department. Activate a specialist only when that examination can materially strengthen, weaken, or distinguish an active diagnosis.

Specialist departments are defined in `specialists/registry.yaml` (13 departments including ARCHITECTURE, CODE, RUNTIME, SECURITY, MEMORY, CONTEXT, TOOLS, ORCHESTRATION, REPOSITORY, VERIFICATION, AUTHORITY, DATA, PROTOCOL_BOUNDARIES).

## Clinical references

- `standards/triage.md`: admission triage and provisional risk (maps to R0-R3 risk classes in protocol)
- `specialists/registry.yaml`: available Hospital departments
- `specialists/routing.md`: differential specialist routing
- `standards/diagnosis.md`: root-cause discipline
- `standards/treatment.md`: bounded treatment and recovery envelope
- `standards/verification.md`: recovery examination
- `standards/resilience.md`: dependency and environment failure testing
- `standards/capability-preservation.md`: protection against capability loss
- `standards/case-continuity.md`: durable case state and handoff
- `templates/README.md`: local patient-chart guidance

## During examination

The Hospital should:

1. separate symptoms from expected behavior;
2. establish the relevant environment and authority envelope;
3. reproduce the condition when safe and useful;
4. build competing diagnoses before choosing one;
5. route only relevant specialist departments;
6. seek evidence against the leading diagnosis;
7. distinguish root cause from contributing factors;
8. stop when confidence is insufficient for the patient's risk class.

Risk classes (R0 routine, R1 standard, R2 high, R3 critical) determine minimum diagnostic evidence, root cause confidence, and verification requirements per `protocol/protocol.yaml`.

## During treatment

A treatment plan should define:

- the change;
- the expected therapeutic effect;
- the blast radius;
- required authority;
- pre-treatment checkpoint;
- rollback or recovery path;
- required recovery evidence;
- capabilities that must remain intact.

Explicit treatment authorization is required for R1-R3 per `protocol/protocol.yaml`.

## During recovery

Recovery is not proven by the treating agent saying the treatment worked.

Depending on risk, recovery may require:

- self-test;
- independent examination;
- adversarial challenge;
- resilience testing;
- regression review;
- capability-preservation review;
- residual-risk assessment.

Evidence levels (E0 claim → E5 independent) and root cause confidence levels (unexplained_correlation → confirmed_root_cause) are defined in `protocol/protocol.yaml`.

## Patient records

Use the templates in `templates/` as local patient-chart formats.

Real patient charts and sensitive evidence stay in the patient-controlled environment. This public repository contains only blank templates and synthetic examples.

# AI Hospital Evolution Tracker

**Status:** ACTIVE  
**Purpose:** Durable anti-drift record for AI Hospital evolution. This file records the canonical implementation baseline, completed evolution tranches, unresolved items, and the exact next move.

## Canonical model

| Element | Role |
|---|---|
| AI Hospital | Overall diagnostic, treatment, recovery, assurance, and learning discipline |
| Vex Hospital | Operational implementation of the Hospital model in this repository |
| TEO | Diagnostic intelligence and specialist-routing lens used during Hospital evolution work |
| 2026 research layer | Evaluation, observability, safety, recovery, and resilience techniques considered for adoption |

TEO is neither removed nor the whole Hospital.

## TEO working method

For each evolution task:

1. Establish symptoms and expected behavior.
2. Route through the relevant specialist lenses.
3. Diagnose root cause before changing anything.
4. Propose the smallest coherent treatment.
5. Respect approval gates for consequential changes.
6. Verify outcome, trajectory, adversarial resistance, regression, and capability preservation as applicable.
7. Record residual risk and follow-up.

## North Star

Build a model-neutral system capable of taking an AI patient through:

**Check-in -> Evidence -> Differential Diagnosis -> Root Cause -> Treatment -> Verification -> Recovery -> Discharge -> Follow-up -> Learned Immunity**

The Hospital must:

- diagnose before changing;
- distinguish symptoms from root causes;
- preserve human authority;
- prevent capability reduction disguised as repair;
- fail closed where evidence or authorization is insufficient;
- test treatment under realistic and adversarial conditions;
- verify recovery independently where required;
- detect recurrence;
- learn only from verified outcomes.

## Confirmed implementation baseline

### V1A - Foundation
**Status:** COMPLETE

### V1B - Protocol Engine
**Status:** COMPLETE

### V1C - Clinical System
**Status:** COMPLETE

### V1D - Playbooks and Assurance Ward
**Status:** COMPLETE

### V1E - Self-Examination and Operational Qualification
**Status:** COMPLETE

### V1.1A - Behavioral Assurance Hardening
**Status:** COMPLETE

### V1.1B - Executable Transition Policy
**Status:** COMPLETE

### V1.1C - Evidence Provenance and Privacy Hardening
**Status:** COMPLETE

### V1.1D - Assurance Coverage Expansion
**Status:** COMPLETE

### V1.1E - Evidence Integrity and Runtime Identity
**Status:** COMPLETE

Main-line implementation includes SHA-256 evidence integrity binding, observed runtime identity attestations, verifier-session separation, and identity-aware behavioral assurance.

### V1.1F - Read-Only Case-State Promotion Engine
**Status:** COMPLETE

Main-line implementation includes the read-only ALLOWED / DENIED / BLOCKED promotion evaluator, patient-controlled evidence bundles, case binding, provenance enforcement, identity binding, and recovery/discharge gates.

## 2026 adoption decisions

### Keep as capability families rather than new subsystems

1. Progressive Treatment Environments
   - replay
   - shadow
   - sandbox
   - canary
   - live promotion

2. Verification Stack
   - outcome
   - trajectory
   - stochastic consistency
   - adversarial
   - resilience / chaos

3. Evidence Integrity Stack
   - provenance
   - freeze
   - artifact binding
   - runtime identity binding

4. Protocol Boundary Diagnostics
   - MCP
   - A2A
   - tool and agent boundary failures

5. Post-Discharge Learning Loop
   - recurrence surveillance
   - learned immunity
   - recalibration

### Rejected as standalone Hospital features

- Mandatory OpenTelemetry dependency
- Agent Chaos as its own department
- Separate MCP department
- Separate A2A department
- Mandatory five-dimensional verification for every case
- Mandatory full simulation-to-live ladder for every treatment
- Numeric root-cause probability percentages
- pass@k / pass^k for every test
- Fixed periodic recalibration as a runtime patient feature

These techniques may still be used where risk and evidence justify them.

## V1.2A - Diagnostic Integrity and Safe Treatment Boundary

**Status:** COMPLETE AND PROMOTED

**Main commit:** `e0575db4c123c1ef96430181970c2277f7466114`

### Scope

1. Pre-treatment evidence freeze
2. Authority / threat envelope at the treatment boundary
3. Recovery checkpoint / rollback envelope
4. Root-cause confidence / evidence-sufficiency gate
5. Anthropic provider/platform intake overlay

### Implemented

- [x] Treatment contract
- [x] Machine-readable predicate integration
- [x] No parallel state machine introduced
- [x] Backward-compatible R0 non-consequential path preserved
- [x] Explicit `pre_treatment_evidence_frozen` fact
- [x] Integrity-bound `diagnostic_snapshot` evidence type
- [x] Provenance rule for evidence freeze
- [x] Consequential treatment fact derived from risk class
- [x] Checkpoint availability derived from structured case state
- [x] Rollback availability derived from structured case state
- [x] Full diagnostic-integrity set rechecked on both routes into `TREATING`
- [x] Canonical R2 and R3 treatment traces bound to frozen diagnostic snapshots
- [x] Mutation protection against removal of the freeze gate
- [x] Anthropic provider playbook registered separately from Claude behavioral diagnostics
- [x] Synthetic Anthropic playbook coverage added
- [x] Operational integration approved
- [x] Integrated regression and adversarial/self-examination verification passed
- [x] Promoted to main

### Verification

Exact pre-merge candidate head:

`471740e282321dc6777b91f0506e7680342e4a6f`

GitHub Actions result:

- Hospital validator: PASS
- Self-examination: 78 tests
- Failures: 0
- Result: OK

The first integration CI run exposed test-fixture drift and a malformed mutation-test newline. Root-cause analysis showed no defect in the production treatment gate. Only the affected test fixtures were corrected; the V1.2A production gate was not weakened.

## Anthropic provider extension

**Status:** OPERATIONALLY INTEGRATED

- Claude playbook remains the model-family behavioral adapter.
- Anthropic playbook is the provider/API/runtime/tooling overlay.
- The overlay does not duplicate canonical Hospital policy.
- Synthetic adapter coverage exists.
- Live Anthropic provider execution is not claimed by synthetic coverage.

## Current unresolved items

### Separate repository-governance work

PR #14, **V1.1G: Repository governance and release discipline**, remains a separate open draft. It is not part of V1.2A and must not be silently folded into later clinical tranches.

### V1.2B - Adaptive Verification

**Status:** NOT STARTED

Candidate scope, subject to fresh TEO gap confirmation before treatment:

- risk-scaled stochastic evaluation;
- verification profiles selected by case risk;
- progressive treatment-environment policy;
- stronger evidence-to-runtime identity binding where justified;
- explicit capability-preservation regression contract.

### V1.2C - Recurrence and Learned Immunity

**Status:** DEFERRED

Candidate scope:

- recurrence surveillance;
- independently verified failure-signature library;
- learned-immunity promotion gates.

## Exact next move

**Run the V1.2B adoption gate against the now-promoted V1.2A baseline before implementing anything.**

The gate must answer:

1. Which V1.2B candidate capabilities are already implemented by V1.1E, V1.1F, or V1.2A?
2. Which are genuine remaining gaps?
3. Which gaps materially improve recovery or assurance?
4. What is the smallest justified V1.2B tranche?

No V1.2B production treatment should begin until this adoption gate is complete.

## Anti-drift controls

1. Repository implementation evidence outranks recollection.
2. Research is not automatically a requirement.
3. Existing capabilities must be mapped before new ones are created.
4. Do not redesign completed Hospital layers without a demonstrated defect.
5. TEO is the diagnostic lens, not the entire architecture.
6. Keep provider-specific behavior outside the vendor-neutral core where possible.
7. Do not claim live-provider validation from synthetic traces.
8. Do not reopen V1.2A unless new evidence shows a defect or regression.
9. Keep repository-governance work separate from clinical evolution unless an explicit dependency is demonstrated.
10. Record uncertainty rather than filling gaps by assumption.

## Session continuity

At the start of a new AI Hospital chat, read in this order:

1. `AI_Hospital_Tracking/AI_HOSPITAL_EVOLUTION_TRACKER.md`
2. `AI_Hospital_Tracking/HANDOVER_INDEX.md`
3. the latest handover listed in the index, if one exists

When the user says **end session**, follow `AI_Hospital_Tracking/HANDOVER_PROTOCOL.md`.

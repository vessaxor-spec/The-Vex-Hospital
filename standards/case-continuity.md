# Case Continuity Standard

## Objective

Make the clinical case recoverable across context resets, model changes, agent handoffs, and long-running work.

The conversation is not the authoritative medical record.

The local case artifacts are.

## Canonical state

The patient-controlled case should maintain:

- current protocol state;
- risk class;
- root-cause confidence;
- authority status;
- active differential diagnosis;
- evidence references;
- treatment status;
- verification status;
- residual risks;
- follow-up needs;
- transition history;
- next required action and blockers.

## State transition history

Record each legal state transition.

A transition record should identify:

- prior state;
- new state;
- time when available;
- evidence that justified the transition;
- authorization reference when applicable.

Do not silently rewrite history to make a case appear cleaner.

Corrections should be additive or otherwise auditable.

## Handoff

A fresh agent or examiner should be able to continue the case from the patient chart and referenced evidence without depending on private reasoning from the previous agent.

A handoff should state:

- what is currently known;
- what remains uncertain;
- the current protocol state;
- the next required action;
- blockers;
- the relevant evidence references.

## Context minimization

Do not copy an entire conversation merely to preserve continuity.

Preserve the facts, state, evidence references, decisions, and authorization needed to continue safely.

Private reasoning is not required for continuity.

## Privacy

Case continuity artifacts remain patient-controlled by default.

Use sanitized references if a case summary must cross into a public or shared context.

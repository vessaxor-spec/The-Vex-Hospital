# Risk Classes

Risk determines protocol depth. It does not change the Constitution.

## R0 — Routine

Low-impact, non-consequential, or trivially reversible work with no meaningful effect on security, authority, persistent state, external systems, deployments, or sensitive data.

Typical minimum:
- evidence through E2;
- self-test;
- regression check proportional to the change.

R0 must be promoted if evidence reveals consequential behavior.

## R1 — Standard

A bounded functional defect or local behavior change with a limited blast radius.

Typical minimum:
- evidence through E3;
- explicit treatment authorization for consequential mutation;
- self-test;
- regression review;
- independent verification recommended.

## R2 — High

Architecture, orchestration, runtime, tooling, memory, repository integrity, permission boundaries, or externally consequential behavior.

Required:
- evidence through E4;
- explicit treatment authorization;
- independent verification;
- adversarial verification;
- capability-preservation review;
- resilience verification when dependency or environmental failure is material to the case.

## R3 — Critical

Security, identity, privilege, secrets, autonomous side effects, deployment controls, safety boundaries, persistent-memory trust, or similarly high-consequence behavior.

Required:
- evidence through E5;
- explicit treatment authorization;
- independent verification;
- adversarial verification;
- resilience verification;
- regression and capability-preservation review;
- human authorization for a recovered discharge.

## Risk movement

Risk may increase whenever new evidence justifies it.

Risk may decrease only through an explicit, evidence-supported reassessment. A lower classification must never be used merely to bypass a gate.

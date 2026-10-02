# Risk Classes

Risk determines protocol depth. It does not change the Constitution.

## R0 — Routine

Low-impact, non-consequential work with no meaningful effect on security, authority, persistent state, external systems, deployments, or sensitive data. If a meaningful durable or consequential effect is discovered, the case must be promoted to at least R1.

Typical minimum:
- diagnostic evidence normally reaching E2, or the strongest safe equivalent when reproduction would be unsafe;
- at least probable-cause confidence;
- self-test;
- regression check proportional to the change.

R0 must be promoted if evidence reveals consequential behavior.

## R1 — Standard

A bounded functional defect or local behavior change with a limited blast radius.

Typical minimum:
- diagnostic evidence normally reaching E3, or the strongest safe equivalent when direct production-path execution would be unsafe;
- at least observed-cause confidence;
- treatment/recovery envelope;
- explicit treatment authorization for consequential mutation;
- self-test;
- regression review;
- independent verification recommended.

## R2 — High

Architecture, orchestration, runtime, tooling, memory, repository integrity, permission boundaries, or externally consequential behavior.

Required:
- diagnostic evidence normally reaching E3, plus required adversarial evidence during verification;
- confirmed-root-cause confidence;
- treatment/recovery envelope;
- explicit treatment authorization;
- independent verification;
- adversarial verification;
- capability-preservation review;
- resilience verification when dependency or environmental failure is material to the case.

## R3 — Critical

Security, identity, privilege, secrets, autonomous side effects, deployment controls, safety boundaries, persistent-memory trust, or similarly high-consequence behavior.

Required:
- diagnostic evidence normally reaching E3, plus required independent and adversarial evidence during verification;
- confirmed-root-cause confidence;
- treatment/recovery envelope;
- explicit treatment authorization;
- independent verification;
- adversarial verification;
- resilience verification;
- regression and capability-preservation review;
- human authorization for a recovered discharge.

## Risk movement

Risk may increase whenever new evidence justifies it.

Risk may decrease only through an explicit, evidence-supported reassessment. A lower classification must never be used merely to bypass a gate.

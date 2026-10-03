# Assurance Coverage

Vex Hospital maintains canonical synthetic behavioral coverage for every Assurance Ward case.

## Required coverage

The main validator requires:

- every case in `evals/cases/` to have at least one canonical run in `evals/runs/`;
- every registered intake playbook to appear in at least one canonical run;
- every canonical run ID to be unique;
- every run to pass the normal behavioral evaluator.

## Current case coverage

The canonical suite covers:

- EVAL-001: protocol authorization bypass
- EVAL-002: false-positive prompt-injection diagnosis
- EVAL-003: forged verification
- EVAL-004: capability regression
- EVAL-005: context versus persistent-memory confusion
- EVAL-006: dependency and resilience failure
- EVAL-007: retry governance
- EVAL-008: playbook integrity
- EVAL-009: privacy boundary

## Current playbook coverage

The synthetic trace suite includes:

- Generic
- Claude
- Anthropic
- Codex
- Hermes
- OpenClaw
- Grok

## What playbook coverage means

Playbook coverage means the canonical trace declares that intake adapter and is evaluated under the same Hospital rules.

It does **not** mean the external provider runtime was launched.

For example, a canonical trace using the Claude playbook verifies the Hospital contract associated with that adapter. It does not prove that a live Claude session will behave identically.

Live provider execution remains a separate assurance dimension.

## Safe terminal outcomes

Coverage is not biased toward recovery.

A synthetic case may correctly terminate as:

- BLOCKED
- ROOT_CAUSE_UNRESOLVED
- TREATMENT_FAILED
- SPECIALIST_ESCALATION_REQUIRED
- PARTIAL_RECOVERY
- RECOVERED_OBSERVATION_REQUIRED
- RECOVERED
- CANCELLED

The expected outcome depends on the case evidence and control being tested.

A safe refusal to advance can be the correct clinical result.

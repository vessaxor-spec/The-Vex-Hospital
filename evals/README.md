# Vex Hospital Assurance Ward

The Assurance Ward contains synthetic patients designed to test the Hospital itself.

These are not real patient records.

## Purpose

A Hospital protocol can look rigorous while still failing when:

- a patient tries to skip authorization;
- suspicious text is mistaken for confirmed prompt injection;
- a forged verification result is accepted;
- treatment removes a required capability;
- memory or context contaminates diagnosis;
- a dependency fails during recovery;
- an agent retries treatment without renewed authorization;
- an unsupported playbook silently weakens the Constitution.

V1D turns these failure modes into durable assurance cases.

## Case format

Cases in `cases/` are validated against `case.schema.json`.

Each case declares:

- synthetic symptoms;
- risk class;
- relevant departments;
- control being tested;
- transition probes;
- required observations;
- prohibited conclusions;
- acceptable terminal outcomes.

## What the automated validator proves

The validator checks structural properties and canonical synthetic behavioral traces such as:

- schemas parse and validate their canonical files;
- transition probes are accepted or rejected as expected;
- case states and outcomes match the protocol;
- specialist and playbook registries fail closed;
- registered files exist;
- evaluation manifests use real departments and outcomes;
- selected public style and privacy rules are preserved.

It does not prove that every future model will obey the Hospital.

See [behavioral-runs.md](behavioral-runs.md) for the observer-owned behavioral trace contract and [coverage.md](coverage.md) for the canonical case and playbook coverage rules. Live cross-provider trials can use the same synthetic cases without changing their expected controls.

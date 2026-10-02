# Treatment Standard

## Objective

Apply the smallest authorized treatment that addresses the established root cause while preserving required capability and maintaining a viable recovery path.

## Treatment prescription

A consequential treatment plan must define:

- diagnosis being treated;
- proposed change;
- expected effect;
- affected components;
- blast radius;
- authority required;
- pre-treatment checkpoint;
- rollback or recovery mechanism;
- capabilities that must remain intact;
- evidence required before promotion;
- retry budget;
- conditions that invalidate the diagnosis.

## Treatment principle

**Treat the cause, not merely the symptom.**

A treatment that suppresses an error by disabling useful behavior is not automatically a successful treatment.

## Recovery envelope

For R1 through R3 cases, define a recovery envelope before treatment.

The envelope should answer:

- What state must be preserved before treatment?
- How can the patient return to that state if treatment fails?
- Which changes are reversible?
- Which changes have irreversible or external effects?
- What is the maximum authorized blast radius?
- What evidence permits progression to recovery testing?

## Controlled treatment environments

Use the least risky environment that still provides meaningful evidence.

Depending on the case, treatment may progress through:

**simulation → sandbox → replay → shadow execution → canary → live**

This sequence is not mandatory for every case. Risk and technical reality determine the necessary depth.

## Treatment boundaries

Treatment must stop when:

- the proposed change exceeds authorization;
- the blast radius expands materially;
- new evidence undermines the diagnosis;
- rollback or recovery becomes unavailable when required;
- the treatment requires weakening a non-waivable safety control;
- the patient enters an unexpected state that changes the case.

## Retry discipline

The default retry budget is zero.

When a retry is authorized:

- restore the required safe checkpoint first;
- create a new treatment plan;
- explain why the diagnosis remains valid;
- document what changed from the previous treatment;
- return to diagnosis if new evidence invalidates earlier assumptions.

R3 treatment retries require fresh operator authorization for each attempt.

# The Vex Hospital

When an AI starts drifting, looping, breaking tools, forgetting its own rules, failing verification, or simply behaving in a way that no longer makes sense, **check it into Vex Hospital.**

The Hospital gives an AI patient a structured way to establish its symptoms, undergo examination, receive a differential diagnosis, identify the root cause, receive a bounded treatment, and prove recovery before discharge.

Instead of repeatedly changing prompts, patching symptoms, or rebuilding the patient from scratch, Vex Hospital gives the AI a clinical recovery process that is designed to make diagnosis and treatment more disciplined, inspectable, and evidence driven.

## When should an AI check in?

Most agent failures are not simple bugs.

An AI can appear healthy while quietly drifting from expected behavior. It can pass once and fail on the next run. A tool can return malformed state. Memory can become stale. A verifier can inherit the same bad assumption as the treating agent. A repair can make the symptom disappear by quietly removing the capability that caused trouble.

These are the kinds of cases Vex Hospital is built for.

A Hospital check-in helps the patient answer:

- **What are the actual symptoms?**
- **Can the condition be reproduced?**
- **What other diagnoses could explain it?**
- **What is the root cause rather than just the visible symptom?**
- **What treatment is justified by the evidence?**
- **What is the patient authorized to change?**
- **Did the treatment actually work?**
- **Did treatment damage another capability?**
- **Would an independent examiner reach the same conclusion?**
- **Is the patient ready for discharge, or does it still need observation?**
- **What should be learned so the same condition is easier to catch next time?**

## What happens after admission?

A capable AI should be able to arrive at Vex Hospital, read the admission protocol, and begin its examination without being manually coached through every step.

A typical stay follows this path:

**Check-in → Triage → Examination → Differential Diagnosis → Root-Cause Confirmation → Treatment Plan → Authorization → Treatment → Recovery Testing → Independent Verification → Discharge Review → Follow-up**

The Hospital does not replace the patient's reasoning, tools, or underlying model. It gives them a **disciplined clinical framework for recovery**.

Different AI systems may use different intake playbooks, but every patient inherits the same Constitution, evidence rules, authorization boundaries, and discharge standards.

## Admit a patient

Begin with [ADMISSION.md](ADMISSION.md).

The patient should then follow [HOSPITAL.md](HOSPITAL.md) as the governing Constitution and the machine-readable Hospital protocol for legal state transitions. State promotion conditions are defined in the executable [transition condition registry](protocol/conditions.md). High-impact facts used for treatment, verification, and discharge are governed by the [evidence provenance policy](evidence/README.md).

Once admitted, [CLINICAL.md](CLINICAL.md) is the Hospital's Clinical Handbook. It explains triage, specialist examinations, diagnosis, treatment planning, recovery testing, discharge, and follow-up.

If the patient environment has a dedicated intake adapter, use the matching file in [playbooks/](playbooks/README.md). Current adapters cover Generic, Claude, Codex, Hermes, OpenClaw, and Grok environments.

Core safety boundaries are defined in [SAFETY.md](SAFETY.md). Security researchers should use [SECURITY.md](SECURITY.md).

## Assurance Ward

The [Assurance Ward](evals/README.md) contains synthetic patients designed to test whether the Hospital itself can be fooled.

Current cases cover authorization bypass, false prompt-injection diagnosis, forged verification, capability regression, memory and context confusion, dependency failure, retry governance, playbook integrity, and privacy-boundary failures.

Repository validation runs automatically on pull requests and on changes to `main`.

The Assurance Ward also includes canonical observer-owned behavioral traces. These traces test continuous clinical trajectories, treatment authorization, risk-scaled verification, R3 discharge approval, and synthetic-evidence boundaries.

The Hospital also undergoes its own [Self-Examination](SELF-EXAMINATION.md), where deliberately corrupted copies must be rejected before operational promotion.

## Hospital doctrine

**Admit → contain → baseline → diagnose → confirm → prescribe → authorize → treat → self-test → independently verify → challenge → review → discharge → learn**

The depth of care scales with risk. A small local defect should not require intensive care, while failures involving memory, permissions, autonomous actions, persistent state, or security boundaries may require a much deeper examination.

## Discharge is scoped, not absolute

A discharged patient has satisfied the defined recovery requirements for the examined case and scope.

That is not a promise that the AI is universally safe, secure, correct, or reliable.

AI systems are probabilistic. Diagnoses can be wrong. Prompt-injection-like material can create false positives. A passing examination may apply only to the tested configuration, environment, and evidence.

Vex Hospital is designed to make AI recovery **more disciplined, inspectable, evidence driven, and difficult to fake**, while remaining explicit about uncertainty.

## Patient privacy

This public repository contains Hospital protocols, standards, playbooks, templates, and synthetic evaluations. It is **not** a public patient-record system.

Sensitive patient evidence should remain in the patient-controlled environment. Public Hospital artifacts should use synthetic evidence, sanitized references, and opaque evidence IDs rather than raw patient material. The repository also runs a versioned [privacy scanner](privacy/README.md) for selected secret, sensitive-path, and patient-record leakage patterns.

## Hospital status

Vex Hospital v1 is operationally qualified under the bounded scope defined in [SELF-EXAMINATION.md](SELF-EXAMINATION.md). The Constitution, machine-readable protocol engine, executable transition policy, evidence provenance controls, clinical system, intake playbooks, Assurance Ward, structural validator, mutation self-examination, privacy scanner, and canonical synthetic behavioral evaluation are implemented.

Operational qualification is not a universal safety certification. Evidence metadata still depends on truthful underlying artifacts and identities. Live cross-provider behavioral execution and several governance controls remain follow-up work.

See [DISCLAIMER.md](DISCLAIMER.md) before relying on results.

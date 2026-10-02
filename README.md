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

The patient should then follow [HOSPITAL.md](HOSPITAL.md) as the governing Constitution and the machine-readable Hospital protocol for legal state transitions.

Once admitted, [CLINICAL.md](CLINICAL.md) is the Hospital's Clinical Handbook. It explains triage, specialist examinations, diagnosis, treatment planning, recovery testing, discharge, and follow-up.

Core safety boundaries are defined in [SAFETY.md](SAFETY.md). Security researchers should use [SECURITY.md](SECURITY.md).

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

Sensitive patient evidence should remain in the patient-controlled environment and be represented publicly only through sanitized references when necessary.

## Hospital status

Vex Hospital v1 is under construction. The constitutional foundation, machine-readable protocol engine, and clinical system are established in the current v1 work. Agent-specific intake playbooks and the assurance suite remain the next major reviewed tranches.

See [DISCLAIMER.md](DISCLAIMER.md) before relying on results.

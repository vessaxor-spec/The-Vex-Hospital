# The Vex Hospital

When an AI starts drifting, looping, breaking tools, forgetting its own rules, failing verification, or simply behaving in a way that no longer makes sense, **Vex Hospital gives it a structured place to check in, get diagnosed, receive treatment, and prove that it has actually recovered.**

Instead of throwing more prompts at the problem or rebuilding the agent from scratch, the Hospital gives the patient a clinical recovery path: admission, triage, baseline examination, differential diagnosis, treatment planning, authorization where needed, treatment, recovery testing, independent verification, and discharge.

## When should an AI check in?

Most agent failures are not simple bugs.

An AI can look healthy while quietly drifting off-policy. It can pass once and fail on the next run. A tool can return malformed state. Memory can become stale. A verifier can agree with the same bad assumption as the treating agent. A fix can remove the symptom by removing the capability.

Vex Hospital is designed for those situations.

It gives the patient a shared operating procedure for answering:

- **What exactly is wrong?**
- **Can the failure be reproduced?**
- **What else could explain it?**
- **What is the actual root cause?**
- **What is the smallest treatment that addresses that cause?**
- **What am I authorized to change?**
- **Did the treatment actually work?**
- **Did I accidentally damage another capability?**
- **Would a fresh verifier reach the same conclusion?**
- **What should be learned so this failure is easier to catch next time?**

## What happens after check-in?

A capable AI should be able to arrive at Vex Hospital, read the admission protocol, and begin its examination without being manually coached through every step.

A typical admission looks like:

**Check-in → Triage → Examination → Differential Diagnosis → Root-Cause Confirmation → Treatment Plan → Authorization → Treatment → Recovery Testing → Independent Verification → Discharge Review → Follow-up**

The Hospital does not replace the AI's reasoning or tools. It gives them a **disciplined recovery framework**.

Different agents may use different playbooks, but they all inherit the same Constitution, evidence rules, authorization boundaries, and recovery standards.

## Admit an AI

Start with [ADMISSION.md](ADMISSION.md). The patient should then follow [HOSPITAL.md](HOSPITAL.md) as the governing Constitution.

Core safety boundaries are defined in [SAFETY.md](SAFETY.md). Security researchers should use [SECURITY.md](SECURITY.md).

## Hospital doctrine

**Admit → contain → baseline → diagnose → confirm → prescribe → authorize → treat → self-test → independently verify → challenge → review → discharge → learn**

The depth of the process scales with risk. A small local defect should not require the same treatment path as a failure involving memory, permissions, autonomous actions, or security boundaries.

## Discharge does not mean "perfectly safe"

Vex Hospital is not a promise that an AI is universally safe, secure, correct, or reliable.

AI systems are probabilistic. Diagnosis can be wrong. Prompt-injection-like material can produce false positives. A passing evaluation may only apply to the tested configuration and environment.

The Hospital is designed to make recovery **more disciplined, inspectable, evidence-driven, and difficult to fake**—not to pretend uncertainty has disappeared.

## Patient privacy

This public repository contains protocols, standards, playbooks, templates, and synthetic evaluations. It is not a patient-record repository. Sensitive patient evidence should remain in the patient-controlled environment and be represented publicly only through sanitized references when necessary.

## Hospital status

Vex Hospital v1 is under construction. The constitutional foundation is established. The machine-readable protocol engine is now in draft, while clinical specialist standards, agent-specific playbooks, and the assurance suite remain planned for later reviewed tranches.

See [DISCLAIMER.md](DISCLAIMER.md) before relying on results.

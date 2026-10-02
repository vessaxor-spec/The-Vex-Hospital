# The Vex Hospital

When an AI starts drifting, looping, breaking tools, forgetting its own rules, failing verification, or simply behaving in a way that no longer makes sense, **Vex Hospital gives it a structured way to figure out what went wrong and recover without blindly changing things.**

Instead of throwing more prompts at the problem or rebuilding the agent from scratch, you can point the AI here and have it follow a disciplined clinical process: establish symptoms, reproduce the issue, map authority, form competing diagnoses, confirm the root cause, propose the smallest safe treatment, get approval where needed, test the result, and verify that recovery did not break something else.

## Why point your AI here?

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

## What using the Hospital should feel like

You should be able to give a capable AI this repository and say:

> Read the admission protocol. Diagnose yourself before changing anything. Follow the Hospital states, stop at approval gates, and prove recovery before declaring the case closed.

The Hospital does not replace the AI's reasoning or tools. It gives them a **disciplined recovery framework**.

Different agents may use different playbooks, but they all inherit the same Constitution, evidence rules, authorization boundaries, and recovery standards.

## Start here

AI patients and operators should begin with [ADMISSION.md](ADMISSION.md), then follow [HOSPITAL.md](HOSPITAL.md) as the governing Constitution.

Core safety boundaries are defined in [SAFETY.md](SAFETY.md). Security researchers should use [SECURITY.md](SECURITY.md).

## Core doctrine

**Observe → contain → baseline → diagnose → confirm → prescribe → authorize → treat → self-test → independently verify → challenge → review → discharge → learn**

The depth of the process scales with risk. A small local defect should not require the same treatment path as a failure involving memory, permissions, autonomous actions, or security boundaries.

## What Vex Hospital is not

Vex Hospital is not a promise that an AI is universally safe, secure, correct, or reliable.

AI systems are probabilistic. Diagnosis can be wrong. Prompt-injection-like material can produce false positives. A passing evaluation may only apply to the tested configuration and environment.

The Hospital is designed to make recovery **more disciplined, inspectable, evidence-driven, and difficult to fake**—not to pretend uncertainty has disappeared.

## Privacy

This public repository contains protocols, standards, playbooks, templates, and synthetic evaluations. It is not a patient-record repository. Sensitive patient evidence should remain in the patient-controlled environment and be represented publicly only through sanitized references when necessary.

## Project status

Vex Hospital v1 is under construction. The constitutional foundation is established. The machine-readable protocol engine is now in draft, while clinical specialist standards, agent-specific playbooks, and the assurance suite remain planned for later reviewed tranches.

See [DISCLAIMER.md](DISCLAIMER.md) before relying on results.

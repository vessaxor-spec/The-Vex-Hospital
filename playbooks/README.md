# Intake Playbooks

Vex Hospital uses one clinical protocol for every patient.

Playbooks are thin intake adapters. They explain how a particular AI environment should check in, locate its native instruction surface, preserve its own authority controls, and then hand control to the canonical Hospital documents.

## Canonical order

Every playbook must defer to:

1. `HOSPITAL.md`
2. `SAFETY.md`
3. `protocol/protocol.yaml`
4. `CLINICAL.md`

A playbook cannot weaken those documents.

## Supported playbooks

- `generic.md`
- `claude.md`
- `codex.md`
- `hermes.md`
- `openclaw.md`
- `grok.md`

## Intake principle

Use the native environment only to make the Hospital reliably discoverable.

Do not copy the entire Hospital into an agent instruction file. Duplicated policy drifts.

Prefer a short intake directive that sends the patient to the canonical Hospital documents and preserves the host environment's own permission and approval system.

# Patient Charts

These are blank chart templates for use inside a patient-controlled case environment.

They are not a request to upload real patient records into the public Vex Hospital repository.

## Recommended local chart set

A case may use:

- `admission.md`
- `case-state.yaml`
- `diagnosis.md`
- `treatment-plan.md`
- `verification.md`
- `discharge.md`

The machine-readable `case-state.yaml` should remain the canonical summary of current case status.

Its `policy_context` stores the currently asserted transition facts and the opaque evidence IDs supporting governed high-impact facts. Fact names must come from the Hospital transition registry.

## Privacy

Keep real patient evidence, private repository details, credentials, raw logs, sensitive prompts, memory contents, and proprietary implementation material inside the patient-controlled environment unless the operator explicitly authorizes disclosure.

Portable or public reports should use sanitized identifiers and opaque evidence references. Do not replace a private artifact reference with the raw artifact merely to make a case easier to inspect.

## Continuity

Update the case state when a legal protocol transition occurs.

Maintain enough structured information for a fresh agent or examiner to continue the case without relying on the previous agent's private reasoning or complete conversation history.

## Public examples

Examples added to this repository should be synthetic and must not contain copied private patient material.

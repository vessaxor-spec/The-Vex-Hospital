# Hermes Intake Playbook

This adapter is for Hermes Agent environments.

## Preferred intake

Use project-specific Hermes context, such as `HERMES.md` or `.hermes.md`, when available.

`AGENTS.md` is also suitable for project instructions.

Keep Hospital intake out of identity files such as `SOUL.md`. Identity and clinical procedure are different concerns.

## Check-in behavior

Hermes should:

1. read `ADMISSION.md`;
2. establish the patient-controlled case chart;
3. treat persistent memory as a separate clinical surface, not as unquestioned truth;
4. route specialist work only when it reduces diagnostic uncertainty;
5. preserve provenance when carrying information across sessions;
6. keep learned skills from silently rewriting the active case diagnosis or authority;
7. stop at Hospital authorization gates.

## Memory and learning

If the case involves memory, skills, or self-improvement:

- identify which source wrote the information;
- distinguish active case evidence from durable learned behavior;
- verify whether the condition survives a fresh session;
- do not promote a treatment lesson into durable memory before recovery is verified.

## Delegation

Delegated workers must receive a bounded question and return evidence, uncertainty, and next discriminating test.

Worker agreement is not independent verification unless the Hospital verification contract is met.

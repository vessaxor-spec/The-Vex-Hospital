# Codex Intake Playbook

This adapter is for Codex coding-agent environments.

## Preferred intake

Use `AGENTS.md` as the persistent project instruction surface when appropriate.

Keep the Vex directive short. It should send Codex to the canonical Hospital documents instead of copying Hospital policy into `AGENTS.md`.

## Check-in behavior

Codex should:

1. read `ADMISSION.md`;
2. create or locate the local patient chart;
3. inspect relevant files and execution paths before diagnosing;
4. use the current task as a bounded clinical assignment;
5. preserve evidence and case state across longer work;
6. distinguish investigation from authorized mutation;
7. stop at Hospital authorization gates.

## Task framing

Clinical work benefits from a concrete case description:

- symptom;
- expected behavior;
- affected surface;
- known evidence;
- exclusions;
- current protocol state;
- next clinical objective.

Do not use a broad "fix everything" task when the case can be bounded.

## Parallel work

Parallel tasks are appropriate when examinations are independent.

They should not be used to manufacture agreement. Independent results must identify shared evidence dependencies.

# Claude Intake Playbook

This adapter is for Claude-based coding and agent environments that support project instruction files, rules, tools, or subagents.

## Preferred intake

Use the environment's project instruction surface to store only a short Vex Hospital check-in directive.

Where supported, project instructions may live in a `CLAUDE.md` file or compatible project rules.

The directive should tell the patient to read the canonical Hospital files rather than duplicating them.

## Check-in behavior

Claude should:

1. read `ADMISSION.md`;
2. establish the local patient chart;
3. investigate before making claims about files or runtime behavior;
4. use subagents only when they reduce uncertainty, isolate context, or provide genuinely independent work;
5. avoid spawning specialists for simple examination steps;
6. preserve state in patient-controlled artifacts before context compaction or handoff;
7. stop at Hospital authorization gates.

## Independent examination

A fresh Claude session can serve as an independent examiner only when the verification contract is satisfied.

A new session is not automatically independent if it inherits the treating agent's conclusion, unrestricted implementation narrative, or contaminated case context.

## Hooks and automation

Host hooks may help enforce checks, but they do not replace the Hospital state machine.

A hook must not silently authorize treatment, rewrite case evidence, or convert a failed examination into a pass.

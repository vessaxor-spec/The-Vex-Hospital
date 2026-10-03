# AI Hospital Session Handover Protocol

## Trigger

Create a handover only when the user says exactly or clearly intends:

**end session**

Do not create one merely because a chat appears to be ending.

## Location

Create the handover in:

`AI_Hospital_Tracking/HANDOVERS/`

## Filename

Use:

`YYYY-MM-DD_HHMM_SESSION_HANDOVER.md`

Use the user's local timezone when available.

## Required structure

Every handover must contain:

1. session date and project
2. objective at session start
3. canonical baseline at session start
4. what was diagnosed
5. what was changed
6. verification performed
7. current canonical state
8. unresolved risks
9. decisions not to revisit without new evidence
10. exactly one primary next move
11. files to read first

## Quality rules

A handover must:

- separate facts from assumptions
- not invent repository state
- not claim tests that did not run
- preserve unresolved uncertainty
- capture exact branches or commits where useful
- remain concise enough for a fresh chat to read before continuing
- identify any archived or superseded work that must not be treated as canonical

## Index maintenance

Every handover must also update:

`AI_Hospital_Tracking/HANDOVER_INDEX.md`

The newest entry goes first and includes:

- timestamp
- filename
- one-line session outcome
- exact next move

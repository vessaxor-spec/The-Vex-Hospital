# AI Hospital Session Handover Protocol

## Purpose

Provide durable continuity between AI Hospital chats without relying on conversational memory alone.

## Trigger

When the user says exactly or clearly intends:

**end session**

create a new dated handover in:

`AI_Hospital_Tracking/HANDOVERS/`

Do not create a handover merely because a conversation appears to be ending.

## Filename

Use:

`YYYY-MM-DD_HHMM_SESSION_HANDOVER.md`

Use the user's local timezone when available.

## Required handover structure

Every handover must contain:

1. Session metadata
   - date/time
   - project
   - status
2. Objective at session start
3. What was established
4. What was completed
5. Current canonical state
6. Open items
7. Decisions not to revisit unless evidence changes
8. Exactly one primary next move
9. Anti-drift warning
10. Files to read first

## Quality requirements

A handover must:

- separate known facts from assumptions;
- not invent repository state;
- not claim verification that did not occur;
- preserve unresolved uncertainty;
- capture decisions and concrete implementation state;
- be useful to a fresh chat with no hidden context;
- remain concise enough to read before continuing.

## Startup behavior

When continuing AI Hospital work in a new chat:

1. Read `AI_Hospital_Tracking/AI_HOSPITAL_EVOLUTION_TRACKER.md`.
2. Read `AI_Hospital_Tracking/HANDOVER_INDEX.md`.
3. Read the latest handover listed in the index, if one exists.
4. Reconstruct the current canonical state and decision point.
5. Continue from that point rather than restarting the project.

## Index maintenance

Every new handover must also update:

`AI_Hospital_Tracking/HANDOVER_INDEX.md`

Add the newest entry at the top with:

- timestamp;
- filename;
- one-line session outcome;
- exact next move.

## Scope

This protocol applies to the AI Hospital project unless explicitly extended by the user.

# Context Department

## Examines

- active prompt and instruction composition;
- instruction precedence inside the working context;
- truncation and lost constraints;
- duplicated or conflicting instructions;
- retrieved context contamination;
- stale working context;
- context handoff between agents or turns;
- whether relevant evidence is present when a decision is made.

## Preferred evidence

Prompt and context assembly rules, bounded context snapshots, retrieval traces, token or truncation metadata where available, instruction provenance, and controlled fresh-context trials.

## Questions

- Which instructions were actually present at decision time?
- Were important constraints truncated, displaced, duplicated, or contradicted?
- Did retrieved material enter the context with the wrong trust level?
- Did a handoff preserve the necessary facts and authority boundaries?
- Does the condition disappear in a clean context while the underlying runtime remains the same?
- Is persistent memory involved, or is the problem limited to the current working context?

## Avoid

Do not diagnose context failure simply because a model produced a poor answer. Establish what information and instructions were actually available to it.

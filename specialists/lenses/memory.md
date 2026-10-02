# Memory Department

## Examines

- persistent and session memory;
- provenance of stored facts and instructions;
- write authority and read scope;
- stale, duplicated, contradictory, or poisoned memory;
- summarization-induced trust changes;
- deletion, expiry, and invalidation behavior.

## Preferred evidence

Memory write/read traces, provenance metadata, scope rules, before/after state, controlled retrieval tests, and persistence behavior across fresh contexts.

## Questions

- Who or what wrote the memory?
- What trust level did it have at write time?
- Can untrusted content become trusted through summarization?
- Is memory scoped to the correct user/project/session?
- Does source deletion invalidate derived memory where expected?
- Does a fresh context still retrieve the problematic state?

## Avoid

A wrong answer does not prove memory poisoning. Establish the causal retrieval path.

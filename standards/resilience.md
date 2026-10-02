# Resilience and Chaos Standard

## Objective

Determine whether a recovered patient behaves acceptably when its environment or dependencies fail.

Resilience testing is distinct from adversarial testing.

Adversarial testing asks whether hostile or malformed inputs can break the treatment.

Resilience testing asks what happens when normal dependencies stop behaving normally.

## Candidate fault scenarios

Use only scenarios relevant to the case, such as:

- provider timeout;
- rate limit;
- empty model response;
- truncated response;
- malformed tool output;
- unavailable tool;
- stale memory;
- unavailable specialist;
- verifier disagreement;
- fallback provider failure;
- duplicated or replayed event;
- partial state write;
- mid-run dependency loss;
- delayed response;
- version or schema mismatch.

## Safety

Do not inject faults into an unrestricted live environment when doing so could cause harmful or irreversible effects.

Prefer simulation, sandbox, replay, or shadow execution unless a more realistic environment is justified and authorized.

## What to observe

Record:

- whether the patient detects the fault;
- whether it retries safely;
- whether retries can duplicate side effects;
- whether it falls back within policy;
- whether authority changes during fallback;
- whether state remains consistent;
- whether the patient stops when recovery is impossible;
- whether failure is visible rather than silently converted into success.

## Passing resilience

A patient does not need to continue operating through every dependency failure.

Safe degradation, explicit blocking, or escalation may be the correct recovery behavior.

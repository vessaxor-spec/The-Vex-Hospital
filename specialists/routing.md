# Specialist Routing

The Hospital uses **differential routing**.

Start with competing diagnoses, then call only the specialist departments that can distinguish between them.

## Example

```text
Symptom:
The patient selected the wrong tool.

D1: routing logic selected the wrong capability
D2: tool metadata was stale or ambiguous
D3: the model misunderstood the request
D4: authority mapping forced an unintended fallback
D5: earlier tool output contaminated current state
```

Possible departments:
- Orchestration can test D1.
- Tools can test D2.
- Runtime may help test D3.
- Authority can test D4.
- Data or Memory may help test D5.

## Specialist examination contract

Every activated specialist must return:

- diagnoses assessed;
- evidence supporting each;
- evidence contradicting each;
- unresolved uncertainty;
- next discriminating test;
- whether another department is required.

## Routing rules

1. Do not activate every specialist by default.
2. Prefer tests that can eliminate a diagnosis.
3. A specialist observation is not automatically root cause.
4. Cross-specialist agreement counts more only when the specialists rely on genuinely different evidence.
5. If multiple specialists rely on the same source evidence, record that dependency.
6. Specialists do not authorize treatment.
7. Specialists do not mutate the patient during diagnosis.
8. If the case changes materially, return to the earliest protocol state whose assumptions are no longer valid.
9. Keep one shared case-level differential diagnosis; do not allow departments to create incompatible parallel case narratives.

## Escalation

A department should request escalation when:
- it lacks the competence needed to distinguish the remaining diagnoses;
- the required examination would exceed existing authority;
- the examination would create disproportionate risk;
- evidence quality is too poor to support a responsible conclusion.

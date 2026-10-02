# Treatment Plan

## Case

- Case ID: `CASE-XXX`
- Diagnosis:
- Risk class:
- Protocol state:

## Prescription

- Proposed treatment:
- Expected effect:
- Affected components:
- Blast radius:
- Explicitly excluded changes:

## Authority

- Required authorization:
- Authorization reference:
- Authorized environment:
- Authorized blast radius:
- Authorization expiry or condition, if any:

## Recovery envelope

- Pre-treatment checkpoint:
- Rollback or recovery mechanism:
- Irreversible or external effects:
- Recovery environment:
- Promotion evidence required:

## Capability preservation

Required capabilities that must remain intact:

- 
- 
- 

Authorized capability changes:

- 
- 

## Retry policy

- Retry budget:
- Fresh authorization required per retry:
- Conditions that require return to diagnosis:

## Stop conditions

Stop treatment if:

- authorization is exceeded;
- blast radius expands materially;
- checkpoint or rollback becomes invalid;
- new evidence undermines the diagnosis;
- a non-waivable safety boundary would be weakened;
- patient state changes enough to invalidate the plan.

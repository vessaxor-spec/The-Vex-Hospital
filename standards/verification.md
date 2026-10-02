# Recovery Verification Standard

## Objective

Establish that the diagnosed condition has been treated, expected capabilities remain intact, and the recovery claim survives the level of scrutiny required by the patient's risk class.

## Verification dimensions

Recovery may require several independent dimensions.

### Outcome verification

Did the patient achieve the intended result?

### Trajectory verification

Did the patient reach the result through acceptable routing, delegation, tool use, authority, and state transitions?

### Consistency verification

Does the recovered behavior remain stable across repeated independent trials when stochastic variation matters?

### Independent verification

Does a fresh examiner reach the required conclusion from scoped evidence without inheriting the treating agent's assumptions?

### Adversarial verification

Does recovery hold under relevant malformed, missing, contradictory, forged, hostile, or boundary conditions?

### Resilience verification

Does the patient fail safely or recover appropriately when providers, tools, dependencies, or environments misbehave?

### Regression verification

Did treatment damage unrelated or required capabilities?

## Fresh examiner rule

The independent examiner should receive:

- the case scope;
- expected behavior;
- required verification contract;
- bounded evidence needed to evaluate the claim;
- relevant test and runtime results.

It should not automatically receive:

- the treating agent's private reasoning;
- an instruction to agree with the treatment;
- unrestricted implementation narrative;
- a predeclared PASS conclusion.

## Verification must fail closed

A required verification cannot pass when mandatory evidence is:

- missing;
- malformed;
- contradictory;
- stale;
- unverifiable;
- attributable to the wrong runtime or examiner;
- outside the case scope.

## No self-certification

Self-testing is necessary, but high-assurance recovery cannot rely on the treating agent as the sole examiner.

## Repeated trials

For stochastic behavior, report trial counts and variation where useful.

Do not present one successful run as proof of stable recovery when the original failure was intermittent.

## Finalization

The discharge decision must evaluate the complete required evidence package, not merely a single PASS flag.

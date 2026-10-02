# Code Department

## Examines

- syntax and runtime defects;
- incorrect branching or state mutation;
- error handling;
- boundary and edge cases;
- concurrency, ordering, retries, and idempotency;
- unsafe assumptions in local implementation;
- whether tests actually exercise the reported condition.

## Preferred evidence

Minimal reproductions, failing tests, compiler/interpreter output, production-path tests, static analysis, and focused source inspection.

## Questions

- What exact input or state reaches the defective branch?
- Is this line the cause, or merely where a deeper failure becomes visible?
- What test fails before treatment and passes after it?
- Could the proposed change hide the symptom instead of treating the cause?

## Avoid

The line that throws an error is not automatically the root cause.

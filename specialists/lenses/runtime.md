# Runtime Department

## Examines

- observed model/provider/runtime identity;
- environment-specific behavior;
- process lifecycle and restart behavior;
- dependency availability, timeouts, and rate limits;
- concurrency and scheduling;
- runtime configuration drift;
- differences between assumed and actual execution.

## Preferred evidence

Observed runtime identity attestations, environment snapshots, traces, dependency responses, timing data, repeated isolated trials, and observed configuration.

## Questions

- What actually ran?
- Which observed identity attestation supports that claim?
- Does the runtime session match or differ from the patient and verifier sessions as expected?
- Does the condition reproduce across runtime identities or environments?
- Did execution state change between trials?
- Is a dependency intermittently degraded?
- Is the runtime using the configuration the operator believes it is using?

## Avoid

Configured identity is not proof of observed runtime identity.

# Architecture Department

## Examines

- component responsibilities and ownership;
- violated invariants;
- state ownership and source-of-truth conflicts;
- configuration and interface contracts;
- hidden dependencies and failure propagation;
- whether a visible symptom is downstream of a deeper structural defect.

## Preferred evidence

Architecture diagrams, configuration contracts, call/data flows, state transitions, interface definitions, and observed production-path behavior.

## Questions

- Which component owns the failing responsibility?
- Which invariant should have prevented the symptom?
- Is state duplicated or ambiguously owned?
- Did a configuration or interface contract drift?
- Can the failure propagate across component boundaries?

## Avoid

Do not diagnose unfamiliarity, complexity, or unconventional design as architectural illness without a violated responsibility, invariant, or contract.

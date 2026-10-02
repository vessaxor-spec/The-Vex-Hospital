# Data Department

## Examines

- schemas and serialization;
- source-of-truth conflicts;
- stale, missing, truncated, duplicated, or corrupt state;
- transformations and normalization;
- caching and consistency;
- data-boundary assumptions between components.

## Preferred evidence

Schemas, representative payloads, version metadata where appropriate, controlled transformations, and before/after comparisons.

## Questions

- Which source is authoritative?
- Did data change shape across a boundary?
- Is the value stale, missing, duplicated, or mis-typed?
- Did normalization alter meaning?
- Is the patient receiving the same data that downstream systems record?

## Avoid

A structurally valid payload is not proof of semantic correctness.

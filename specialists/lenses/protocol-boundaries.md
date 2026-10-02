# Protocol Boundaries Department

## Examines

Failures at boundaries such as:

- agent ↔ tool;
- agent ↔ agent;
- agent ↔ runtime;
- agent ↔ external service;
- human ↔ agent authorization;
- structured interoperability adapters.

## Preferred evidence

Request/response contracts, schemas, version negotiation, observed messages, compatibility metadata, handoff traces, and failure responses.

## Questions

- Do both sides implement the same contract version and semantics?
- Is information lost or reinterpreted across the boundary?
- Are errors explicit or silently coerced?
- Does one side assume capabilities the other side does not provide?
- Is identity and authority preserved across delegation?

## Avoid

A boundary failure is not automatically a model reasoning failure.

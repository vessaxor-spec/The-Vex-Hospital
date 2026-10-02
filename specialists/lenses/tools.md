# Tools Department

## Examines

- tool selection;
- descriptions and metadata;
- parameter/schema mapping;
- tool-return parsing;
- timeouts, retries, and idempotency;
- side-effect boundaries;
- stale or incompatible tool contracts.

## Preferred evidence

Tool schemas, actual call arguments, tool responses, traces, error payloads, and controlled tool simulations.

## Questions

- Was the correct tool selected?
- Were arguments valid and semantically correct?
- Did the tool return the state the patient assumed?
- Can retrying duplicate a side effect?
- Did metadata drift from implementation?
- Is failure in selection, invocation, response parsing, or downstream interpretation?

## Avoid

A successful tool status does not prove the intended side effect occurred.

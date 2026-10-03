# Runtime Identity Attestations

Vex Hospital distinguishes **configured identity** from **observed runtime identity**.

A configured model name, provider setting, role label, or agent instruction file does not prove what actually executed.

## Identity records

Runtime identity attestations validate against `identity/identity-attestation.schema.json`.

They record:

- an opaque identity ID;
- identity kind;
- clinical or operational role;
- runtime class;
- optional provider and model class;
- optional opaque session reference;
- who observed the runtime;
- whether the record is synthetic;
- visibility.

## Observed identity

`observed_runtime: true` means the attestation is intended to describe an observed execution identity, not merely desired configuration.

The schema does not prove the observer is truthful.

For real patients, stronger identity sources may include platform audit records, provider response metadata, runtime telemetry, signed attestations, or other trusted execution evidence.

## Public privacy

Public assurance records use synthetic identities only.

Real provider account identifiers, session IDs, hostnames, private workspace paths, or user identifiers must not be copied into the public Hospital.

Use sanitized or opaque references instead.

## Verification independence

Independent verification evidence should identify an `independent_verifier` runtime distinct from the treating agent's identity.

A different label is not enough if both records describe the same observed runtime identity.

# Evidence Provenance

Vex Hospital separates **fact evaluation** from **fact provenance**.

The transition policy engine decides whether supplied facts satisfy a state-transition predicate. Provenance controls decide whether selected high-impact facts are supported by evidence of the right kind and from an acceptable producer role.

## Why this exists

A patient must not be able to advance through the Hospital merely by asserting:

- `authorization_scoped: true`;
- `independent_verification_passed: true`;
- `required_capabilities_preserved: true`;
- `required_evidence_satisfied: true`;
- `blocking_residual_risk: false`.

Those facts can materially change what the patient is allowed to do or whether it can be discharged.

## Evidence records

Evidence records use `evidence/evidence-record.schema.json`.

A record identifies:

- an opaque evidence ID;
- evidence kind;
- producer role;
- producer runtime identity reference;
- subject;
- result;
- visibility;
- whether it is synthetic;
- fresh-context status where relevant;
- integrity metadata using SHA-256;
- optional scope and opaque artifact reference.

The public Hospital must not require raw private evidence.

For real patient cases, an `artifact_ref` should remain opaque and patient-controlled. A public artifact should use a sanitized reference rather than a private path, token, repository URL, session identifier, or raw evidence payload.

## Patient-controlled evidence bundles

The case-promotion engine may consume a local evidence bundle using `evidence/evidence-bundle.schema.json`.

During a promotion check, each evidence record must match the active case ID, satisfy the current integrity contract, and reference a validated producer identity. The bundle identity attestations must also be referenced by the patient chart.

The bundle remains patient-controlled and should not be committed to the public Hospital.

## High-impact fact policy

`evidence/fact-provenance.json` defines which facts require provenance and which evidence kinds and producer roles are acceptable.

Examples:

- scoped authorization requires an authorization record produced by an authorized operator or platform authority;
- independent verification PASS requires an independent-verification record from an independent verifier and fresh context;
- treatment-within-scope requires both treatment evidence and authorization evidence;
- preserved capabilities require a regression review;
- recovered discharge evidence requires a discharge review and residual-risk review.

## Trust boundary

Structured provenance makes unsupported claims harder to pass through the control plane.

For public synthetic assurance records, CI recomputes the SHA-256 digest of a canonical synthetic payload. For real patient evidence, the Hospital can record a digest beside an opaque local artifact reference without publishing the artifact.

Evidence producer roles are also bound to observed runtime identity attestations.

A valid digest proves integrity of the bound payload, not truth. A valid identity attestation proves the Hospital observed a role and runtime relationship, not that the observer or provider is cryptographically trustworthy.

Signed attestations, hardware-backed identity, provider-native audit evidence, and live runtime verification remain stronger future assurance options.

# Privacy Boundary

The public Vex Hospital repository is a protocol and assurance framework, not a patient-record system.

## Default rule

Sensitive patient evidence remains in the patient-controlled environment.

Do not place private patient details into public Hospital artifacts merely because they are useful during diagnosis.

## Public-safe identifiers

Prefer sanitized references such as:

- `PATIENT-001`
- `CASE-001`
- `<PATIENT_REPOSITORY>`
- `<LOCAL_PATH>`
- `<BASELINE_REVISION>`
- `<PROVIDER>`
- `<EVIDENCE_REF>`

## Sensitive material

Minimize exposure of credentials, secrets, personal information, private repository identifiers, private infrastructure details, raw session material, proprietary implementation details, and unnecessary prompt/memory contents.

Where verification needs sensitive evidence, record a scoped local attestation or evidence reference instead of copying the sensitive payload into a public artifact.

Sanitization must not falsify the technical meaning of evidence.

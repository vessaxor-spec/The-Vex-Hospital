# Verification Department

## Examines

- false-positive recovery;
- verifier independence;
- evidence completeness;
- forged, stale, or incomplete attestations;
- self-test presented as independent verification;
- verifier identity and execution path;
- whether required negative and adversarial cases were actually exercised.

## Preferred evidence

Fresh verification runs, verifier inputs, observed verifier identity attestations, evidence digests, structured attestations, failure-case tests, and finalization logic.

## Questions

- Was the verifier genuinely fresh?
- Is the verifier runtime identity distinct from the patient runtime session?
- Does the verification evidence digest match the bound payload?
- Did it inherit the treating agent's conclusion?
- Is it evaluating bounded evidence or the treating agent's narrative?
- Can missing evidence fail open?
- Can a forged PASS or partial attestation reach discharge?
- Does final success require all required recovery conditions?

## Avoid

A second model call is not automatically independent verification.

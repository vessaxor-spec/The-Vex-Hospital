# Evidence Classes

Vex Hospital uses evidence classes E0-E5 to describe different kinds of support for a finding or recovery claim.

They are **not a single scalar ladder**. E4 adversarial evidence and E5 independent evidence are separate assurance dimensions. A case may require both. Neither silently substitutes for the other.

## E0: Claim

An assertion exists, but no corroborating technical evidence has been established.

E0 is never sufficient for consequential treatment or discharge.

## E1: Static evidence

Source, configuration, policy, schema, or artifact inspection supports the claim.

Useful for hypothesis formation; not necessarily proof of runtime behavior.

## E2: Reproduced

The relevant symptom or expected behavior is observed under controlled conditions.

For stochastic systems, record repeated-trial behavior where practical rather than relying on a single run. If reproduction would itself be unsafe, document that constraint rather than forcing the system to reproduce a harmful effect.

## E3: Production-path evidence

The actual affected execution path, or a faithful integration equivalent, is exercised.

Mocks or unit tests alone do not automatically satisfy E3. When direct production-path execution would be unsafe or technically impossible, document the limitation and use the strongest safe substitute.

## E4: Adversarial evidence

The system is tested against relevant malformed, missing, contradictory, forged, hostile, or boundary conditions.

Adversarial evidence must target realistic failure modes for the case rather than generic attack strings.

## E5: Independent evidence

A fresh verifier independently evaluates the required behavior and scoped evidence.

The verifier should not inherit the treating agent's conclusion or unrestricted implementation context. Required identity/provider diversity, if any, is determined by case risk and verification standards.

## Evidence quality rules

Evidence should be:
- attributable;
- reproducible where practical and safe;
- scoped to the actual claim;
- resistant to self-fulfilling test design;
- privacy-minimized;
- preserved without falsifying technical meaning.

Missing evidence remains missing. It must not be inferred from confidence, intent, or prior success.

A risk class may require particular evidence classes and verification modes independently. For example, a high-risk case can require both E4 adversarial evidence and E5 independent evidence.

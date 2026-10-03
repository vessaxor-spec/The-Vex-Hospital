# Vex Hospital Self-Examination

Before Vex Hospital v1 can be described as operational, the Hospital must undergo its own examination.

This is an operational qualification, not a universal safety certification.

## Patient

**Patient:** Vex Hospital itself

**Presenting question:** Can the Hospital detect selected failures in its own control plane, or can a malformed change pass while violating its stated invariants?

## Qualification criteria

V1 operational qualification requires:

1. the clean Hospital validator passes;
2. protocol, transition-policy, case-promotion, runtime-identity, evidence-integrity, evidence-provenance, governance-policy, specialist, playbook, patient-chart, assurance-case, privacy-policy, behavioral-run, and style checks pass in CI;
3. deliberate mutation of a protected treatment gate is detected;
4. an undeclared specialist department is rejected;
5. patient-chart and protocol-state drift is detected;
6. tampering with an assurance-case expected result is detected;
7. an undeclared playbook is rejected;
8. selected sensitive-path leakage is detected;
9. retired public narrative wording is detected;
10. the project no-em-dash rule is enforced;
11. the clean repository still passes after the mutation suite;
12. known residual risks are recorded rather than hidden.

## Mutation method

The self-examination never corrupts the live branch.

Each test copies the Hospital into an isolated temporary directory, introduces one known-bad mutation, executes the same validator used by CI, and expects the validator to fail.

A mutation test itself passes only when the corrupted Hospital is rejected.

## What this proves

The suite provides evidence that selected Vex controls are enforceable rather than purely descriptive.

It specifically tests whether the current validator detects known classes of control-plane drift.

## What this does not prove

This qualification does not prove:

- that every AI model will obey Vex Hospital;
- that every possible prompt injection, tool failure, memory issue, or security vulnerability is detected;
- that a future protocol defect cannot evade the current assurance suite;
- that all supported agent runtimes behave identically;
- that the Hospital replaces platform security controls or operator judgment.

Cross-provider behavioral runs remain a separate assurance dimension.

## Known residual risks

Operational qualification does not remove these known limitations:

- every Assurance Ward case and every registered intake playbook has canonical synthetic behavioral coverage, but live cross-provider behavioral runs are not yet automated in CI;
- the mutation suite covers selected control failures, not every possible protocol defect;
- high-impact facts are bound to typed evidence, SHA-256 integrity metadata, and observed runtime identity attestations, but cryptographic producer authenticity and provider-native identity proof are not yet guaranteed;
- privacy scanning is stronger and registry driven, but it remains pattern based and is not a guarantee that every secret or private artifact will be detected;
- supported agent environments may change their native instruction, tool, memory, or permission conventions;
- repository governance is version controlled and CI checked, but live GitHub branch protection and ruleset enforcement remain unverified and are not enabled by the policy files themselves;
- the project license remains unresolved, so the project must not claim open-source status.

These items do not invalidate the structural qualification, but they define its scope and follow-up needs.

## Operational outcome

The Hospital may be labeled **v1 operational** only when the clean validator and all required self-examination mutation tests pass on the exact candidate revision.

Any required mutation test that unexpectedly passes is a qualification failure and must be investigated before promotion.

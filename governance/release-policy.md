# Release Discipline

A Vex Hospital release is a promotion of a specific, verified repository revision.

A release should not be created from an arbitrary working tree, unverified branch, or moving branch name.

## Release candidate

A release candidate must identify:

- semantic version;
- exact 40-character commit SHA on `main`;
- successful Hospital validation;
- completed self-examination;
- known residual risks;
- license status;
- whether an open-source claim is being made.

Release manifests must validate against `governance/release-manifest.schema.json`.

## Promotion gate

Before tagging a release:

1. the candidate commit must be on `main`;
2. the Hospital validation workflow for that exact commit must pass;
3. the self-examination for that exact commit must pass;
4. the changelog must describe the release-relevant changes;
5. known residual risks must be recorded;
6. the release manifest must validate;
7. an open-source claim must not be made while license status is unresolved.

## Tags

Release tags use:

`vMAJOR.MINOR.PATCH`

Optional prerelease suffixes may be used when appropriate.

The tag should identify the exact verified `main` commit recorded in the release manifest.

## Release claims

A release may be described as operationally qualified only within the scope of the tests and controls that passed for that exact revision.

Do not turn a release tag into a universal safety, security, correctness, or reliability claim.

## Rollback and withdrawal

If a released control-plane defect is later found:

- record the defect;
- identify affected release revisions;
- admit the Hospital itself as a patient when appropriate;
- create a bounded corrective tranche;
- preserve the failed condition as a regression or Assurance Ward case where useful;
- clearly mark superseded or withdrawn release guidance.

Do not silently rewrite release history.

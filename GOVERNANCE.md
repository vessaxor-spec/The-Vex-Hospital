# Repository Governance

Vex Hospital treats its own repository as part of the Hospital control plane.

This document describes the intended governance model for source changes and releases.

It does **not** claim that equivalent GitHub branch protection or rulesets are currently enabled.

The machine-readable desired policy is in `governance/repository-policy.json`.

## Main branch

The intended operating model for `main` is:

- changes arrive through pull requests;
- direct pushes are not part of the normal change path;
- the Hospital validation job must pass before promotion;
- the full self-examination remains part of that validation;
- squash merge is the preferred promotion method;
- force pushes and branch deletion are not permitted by the desired live policy;
- conversation resolution is required before promotion;
- linear history is preferred.

These are version-controlled governance requirements.

Live GitHub enforcement remains a separate repository-setting action and must be approved before activation.

## Solo-maintainer reality

The current repository may be operated by a single maintainer.

Governance must not create a fake independence claim by requiring the author to approve their own pull request.

The intended model therefore relies on:

- machine-enforced Hospital checks;
- explicit review comments recording scoped verification;
- PR-based promotion;
- external maintainer review for third-party contributions;
- separate authorization for consequential repository-setting changes.

If additional maintainers are added later, review requirements can be strengthened.

## Required assurance

A change is not ready for promotion merely because it compiles or looks reasonable.

The governance policy requires:

- Hospital validation;
- self-examination;
- privacy-policy checks;
- case-promotion contract validation.

Additional checks may be added without weakening these requirements.

## Live enforcement boundary

This repository policy is declarative.

It does not turn on branch protection, GitHub rulesets, required reviews, merge restrictions, secret scanning, or other GitHub account settings by itself.

Those settings can materially affect repository access and recovery. They require a separate approved configuration step.

## License status

The repository currently has no selected project license.

Do not describe Vex Hospital as open source unless an appropriate license has been selected and documented.

Public visibility is not the same as permission to reuse, modify, or redistribute the project.

License selection remains a separate legal and distribution decision.

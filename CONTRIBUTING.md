# Contributing

Vex Hospital is a public project, but the project license is currently unresolved.

## Before contributing code

Do not assume that public visibility means the repository is open source.

Until a project license is selected, maintainers should not merge substantial third-party code contributions without resolving the applicable contribution and licensing terms.

Issues, bug reports, design feedback, and security reports remain welcome through the appropriate GitHub channels.

## Pull requests

A proposed change should explain:

- the symptom, gap, or control being addressed;
- the expected behavior;
- the bounded scope of the change;
- whether patient privacy, authority, evidence, protocol states, or verification are affected;
- tests or assurance cases added or updated;
- known residual risks.

Do not include real patient records, private repository details, credentials, raw session material, or private evidence.

## Clinical discipline

Changes to Vex Hospital should follow the same principles the Hospital applies to patients:

- establish the problem before changing the control plane;
- prefer bounded changes;
- preserve existing capability unless removal is intentional and justified;
- verify behavior;
- add regression coverage for meaningful failures;
- disclose unresolved risks.

## Style

- Do not use em dash characters.
- Do not revive retired pointer-style intake wording. Keep admission language aligned with the Hospital check-in theme.
- Keep the Hospital theme clear without weakening technical precision.
- Avoid universal safety or certification claims.

## Security findings

Use the guidance in `SECURITY.md`.

Do not publish working exploits against real patient systems or include private patient evidence in a public issue.

# Vex Hospital Template

Use this template to bootstrap a new Vex Hospital-compliant AI clinical recovery project.

## What this template provides

- ✅ Complete Vex Hospital protocol (`protocol/protocol.yaml`)
- ✅ Schema validation pipeline (JSON Schema + Python)
- ✅ Evidence provenance & integrity (DSSE + Sigstore)
- ✅ Privacy scanning (500+ secret patterns)
- ✅ Self-examination mutation tests (12 mutations)
- ✅ CI/CD with linting, type checking, unit tests, integration tests
- ✅ Semantic Release automation
- ✅ Doc-sync validation

## Quick start

1. Click "Use this template" → "Create a new repository"
2. Clone your new repo
3. Run validation locally:
   ```bash
   python -m venv .venv
   .venv/bin/pip install -r requirements.txt
   python scripts/validate_hospital.py
   ```
4. Configure branch protection on `main`:
   - Require status checks: `lint`, `validate`, `test`, `integration`, `self-examination`
   - Require signed commits
   - Require linear history

## Structure

```
.
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   └── template/           # This template metadata
├── protocol/               # Machine-readable protocol
│   ├── protocol.yaml       # Main protocol (states, transitions, risk classes)
│   ├── conditions/         # Modular transition conditions
│   └── *.schema.json       # JSON Schemas
├── evidence/               # Evidence provenance & integrity
├── privacy/                # Privacy scanning patterns
├── specialists/            # 13 specialist departments
├── playbooks/              # 6 intake adapters
├── evals/                  # Assurance Ward (9 synthetic cases)
├── live_trials/            # Provider-neutral trial harness
├── templates/              # Patient chart templates
├── scripts/                # Validation & build scripts
├── tests/                  # Unit, integration, mutation tests
├── requirements.txt        # Pinned Python dependencies
├── package.json            # Node.js dev dependencies
└── .releaserc.json         # Semantic Release config
```

## Protocol versioning

This template uses **Semantic Versioning** via conventional commits:
- `feat:` → minor version bump
- `fix:` → patch version bump
- `BREAKING CHANGE:` → major version bump

Releases are automated via Semantic Release on push to `main`.

## Customization

1. **Add specialist lenses** in `specialists/lenses/`
2. **Add intake playbooks** in `playbooks/`
3. **Add assurance cases** in `evals/cases/`
4. **Extend privacy patterns** in `privacy/sensitive-patterns.json`
5. **Modify risk classes** in `protocol/protocol.yaml`

## License

[MIT](LICENSE) -- or choose your own.

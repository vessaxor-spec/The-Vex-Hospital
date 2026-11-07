# AI Hospital Evolution Tracker

**Status:** ACTIVE  
**Purpose:** Durable anti-drift record for Vex Hospital evolution.

## Canonical baseline

**Last independently qualified clinical baseline:** V1.2A: Provider-Neutral Live Behavioral Trial Harness

Qualified baseline commit:

`9d8a6687aed787b8910a4b09db2e013bc3ab3a46`

**Current deployed main head at the 2026-11-07 audit:** `d0ba0010ff20b31f4aecad49271865c6902bce69`

The branch later received the 2026-10-04 v2.0 migration and CI/security/release changes.
These are present on `main` but **not qualified** by an end-to-end passing CI run.
Do not confuse the latest deployed source with the last qualified baseline.

## Completed sequence

- V1A: Foundation
- V1B: Machine-readable Protocol Engine
- V1C: Clinical System
- V1D: Playbooks and Assurance Ward
- V1E: Hospital Self-Examination and Operational Qualification
- V1.1A: Behavioral Assurance Hardening
- V1.1B: Executable Transition Policy
- V1.1C: Evidence Provenance and Privacy Hardening
- V1.1D: Assurance Coverage Expansion
- V1.1E: Evidence Integrity and Runtime Identity
- V1.2A: Provider-Neutral Live Behavioral Trial Harness

The 2026-10-04 v2.0 migration is implemented on `main` but awaits qualification.

## Canonical capabilities at V1.1E

The Hospital currently includes:

- Constitution, authority model, privacy rules, and Safety Covenant
- machine-readable protocol and legal state transitions
- executable transition predicates
- specialist routing and clinical standards
- risk classes and evidence requirements
- patient charts
- Generic, Claude, Codex, Hermes, OpenClaw, and Grok intake playbooks
- Assurance Ward synthetic cases
- observer-owned behavioral traces
- behavioral coverage for every current Assurance Ward case
- behavioral representation of every registered playbook
- evidence provenance for high-impact facts
- privacy and sensitive-content scanning
- SHA-256 evidence integrity binding for synthetic assurance records
- observed runtime identity attestations
- independent-verifier session separation
- mutation self-examination and CI validation

## Drift incident

A separate line of work advanced beyond V1.1E without staying aligned to the original roadmap.

That line added items labeled V1.1F and V1.2A and then wrote a tracker that declared those additions canonical.

That lineage is **not canonical**.

It is preserved only for forensic reference at:

`archive/drifted-main-2026-10-03`

Do not copy, merge, or revive work from that archive unless a fresh gap analysis independently justifies the specific capability.

## Original unresolved areas after V1.1E

### 1. Live cross-provider behavioral trials

Synthetic behavioral coverage exists.

What is not yet proven is live behavior across real external runtimes such as Claude, Codex, Hermes, OpenClaw, Grok, or future providers.

Any live trial framework must preserve:

- explicit authorization
- credential isolation
- cost limits
- synthetic patients only unless separately approved
- runtime identity capture
- independent verification
- no public patient evidence

### 2. Repository governance

Branch protection, rulesets, release discipline, and merge policy remain legitimate governance topics.

They are separate from clinical evolution and must be reconsidered from the corrected baseline.

### 3. License

The project license remains unresolved.

This is a separate legal and distribution decision.

## Post-V1.1E adoption gate

**Status:** COMPLETE

### Findings

Already implemented by V1.1A through V1.1E:

- executable transition policy
- evidence provenance
- privacy controls
- behavioral trace evaluation
- full synthetic Assurance Ward case coverage
- playbook coverage
- evidence integrity binding
- observed runtime identity and verifier-session separation

Genuine remaining technical gap:

- provider-neutral execution of behavioral trials through real external runtimes

Separate non-clinical topics:

- repository governance
- project license

Rejected as the next step:

- another case-promotion or parallel control-plane subsystem

### Selected next tranche

**V1.2A: Provider-Neutral Live Behavioral Trial Harness**

Goal:

Create the smallest safe execution boundary that can later host real provider adapters without changing the canonical behavioral evaluator.

V1.2A must:

- remain synthetic-only by default
- require per-run authorization for future live execution
- isolate adapter execution in a temporary workspace
- filter credential environment variables
- enforce declared network policy and budgets
- reuse existing behavioral assurance instead of creating another verification stack
- ship with mock adapters only until a provider-specific adapter is separately reviewed

## V1.2A verification

**Status:** COMPLETE AND PROMOTED

Main commit:

`9d8a6687aed787b8910a4b09db2e013bc3ab3a46`

Verification:

- Hospital validator: PASS
- trial-harness validation: PASS
- self-examination: 63 tests
- failures: 0
- result: OK

Implemented:

- provider-neutral trial manifest
- adapter registry
- subprocess trial worker
- temporary workspace
- filtered credential environment
- per-run live authorization gate
- timeout and reported usage budgets
- checked-in mock-only manifests
- returned trace evaluation through the existing Hospital behavioral evaluator

No real provider adapter is registered. V1.2A does not constitute live-provider validation.

## Post-V1.2A deployed changes and recovery gate (2026-11-07 audit)

**Status:** CI RECOVERY IN PROGRESS; v2.0 deployment NOT QUALIFIED.

The 2026-10-04 history contains a v2.0 migration (commit `94e32b3a9f529bd548cf5f2b0723e1a38d4db8fd`) with:
- modular condition definitions and build logic;
- property-based and schema evolution tests;
- document synchronization and full-journey tests;
- versioned evidence-envelope and expanded privacy-scanner material;
- GitHub release, dependency/security, and SBOM/provenance workflow definitions.

The latest main commit in the audit is `d0ba0010ff20b31f4aecad49271865c6902bce69`.
The `package.json` version is `2.0.0`, but `CHANGELOG.md` contains a release headed `1.0.0`.
Version naming and release claims are not substitutes for successful verification.

Observed failures in the scheduled 2026-11-02 validation run:
- `ruff.toml` used `[tool.ruff]` in a standalone file, which Ruff rejects;
- JSON security reports were uploaded to a SARIF-only action, and some reports were missing;
- the status-check job printed success without examining its upstream jobs;
- the new commit linter re-checked legacy history against a later-adopted policy;
- separate security/release/SBOM workflow reliability has not been established.

A bounded CI remediation branch is being prepared. Do **not** mark CI recovered until:
1. pull-request and scheduled validation execute real tests and report all required job results accurately;
2. no scan failure is disguised by an artifact-upload error or unconditional success;
3. outstanding security, release and provenance workflow failures are separately triaged;
4. the exact verified candidate head is recorded.

No external live provider adapter is registered. A green mock harness is not live-provider proof.

## Exact next move

**First:** restore trustworthy CI and qualify or reject the deployed v2.0 implementation using actual passing tests and recorded evidence. Do not merely disable failing jobs. After that gate passes, run a **live adapter selection gate**.

The gate must choose at most one initial external runtime for the first real provider adapter and must evaluate:

1. current operator access and authorization
2. credential handling
3. provider or runtime API stability
4. network and side-effect envelope
5. cost controls
6. observed runtime identity evidence
7. ability to produce the canonical behavioral-run contract

Do not build multiple live adapters in parallel. Do not claim cross-provider validation from the mock harness.

## Anti-drift rules

1. Repository evidence outranks recollection.
2. Completed V1.1A through V1.1E work is not redesigned without a demonstrated defect.
3. TEO is the diagnostic lens, not the entire architecture.
4. Research ideas are candidates, not automatic requirements.
5. Existing capabilities must be mapped before new components are created.
6. Synthetic coverage must never be described as live-provider validation.
7. Capability removal must not be disguised as treatment.
8. Authority must not be inferred from tool availability.
9. Archived drifted work is reference material only.
10. Consequential repository changes require an explicit recovery path and verification.

## Session continuity

At the start of a new AI Hospital chat, read:

1. `AI_Hospital_Tracking/AI_HOSPITAL_EVOLUTION_TRACKER.md`
2. `AI_Hospital_Tracking/HANDOVER_INDEX.md`
3. the latest handover listed in the index, if one exists

When the user says **end session**, follow `AI_Hospital_Tracking/HANDOVER_PROTOCOL.md`.

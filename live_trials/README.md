# Behavioral Trial Harness

Vex Hospital uses this harness to execute provider-neutral behavioral trials through registered adapters.

## Current V1.2A boundary

V1.2A implements the execution harness and mock adapters used by CI.

**No real provider adapter is registered yet.**

Therefore V1.2A does not claim live Claude, Codex, Hermes, OpenClaw, Grok, or other provider validation.

## Safety model

Every checked-in trial manifest must be:

- synthetic only
- mock execution
- isolated in a temporary workspace
- free of external side effects
- explicit about network policy
- bounded by timeout, request, tool-action, and cost limits

Live execution is fail-closed.

A future live adapter must:

- be explicitly registered as live-capable
- not be test-only
- declare whether it requires network access
- declare the credential environment names it needs
- receive explicit per-run operator authorization
- receive only the declared credential environment variables
- return a behavioral run that passes the existing Hospital evaluator

## Credential isolation

Credential values are never stored in trial manifests or the adapter registry.

The runner passes only credential environment variables declared by the selected adapter.

Unrelated host environment variables are not forwarded to the adapter subprocess.

## Important limitation

The V1.2A subprocess boundary is not an operating-system security sandbox.

Repository adapter code is trusted Hospital code. A future live adapter still requires code review and provider-specific threat analysis before registration.

## Example

The checked-in mock manifest can be run with:

`python scripts/run_live_trial.py live_trials/manifests/TRIAL-EVAL-001-MOCK.json`

The result reports only the trial summary and usage. The full adapter trace is evaluated in a temporary workspace and is not published by default.

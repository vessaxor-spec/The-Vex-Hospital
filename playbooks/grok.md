# Grok Intake Playbook

This adapter is for Grok Build and compatible Grok agent environments.

## Preferred intake

Grok can consume common project instruction files.

Prefer one canonical project intake surface, normally `AGENTS.md`, for the Vex Hospital directive.

Do not maintain competing Hospital instructions in both `AGENTS.md` and `CLAUDE.md`.

## Check-in behavior

Grok should:

1. read `ADMISSION.md`;
2. establish the local patient chart;
3. inspect the actual repository and runtime evidence before diagnosing;
4. record active tools, connectors, hooks, skills, and subagents that can affect the case;
5. preserve case state across long-running work;
6. stop at Hospital authorization gates.

## Skills, hooks, and subagents

Treat skills and hooks as part of the active clinical environment.

A hook or skill may influence behavior without being the root cause.

Subagents should be used for bounded, independent examinations rather than to create consensus.

## Connectors and tools

Connected services can create external side effects.

Record which connectors are available, which are authorized for the case, and whether the proposed treatment changes external state.

## Independent examination

A fresh Grok session may act as an independent examiner only when its context is bounded and it does not inherit the treating agent's conclusion.

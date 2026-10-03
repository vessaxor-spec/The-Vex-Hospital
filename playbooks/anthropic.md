# Anthropic Provider Playbook

This adapter covers Anthropic provider and platform integration boundaries for Claude-family deployments.

It does not replace the Claude model-family playbook. Use `claude.md` for model-behavior diagnosis and this playbook only when the suspected failure may sit at the provider, API, runtime, or tool-integration boundary.

## Preferred intake

1. follow the canonical Hospital admission flow;
2. apply the Claude playbook for model-family behavioral questions;
3. use this provider overlay only for Anthropic-specific integration evidence;
4. keep credentials, raw private traces, and sensitive patient material outside the public Hospital repository.

## Provider-boundary examination

Distinguish model behavior from integration behavior before assigning root cause.

Check, where relevant:

- provider/API request and response boundaries;
- configured model/provider class versus observed runtime identity;
- authentication and permission scope without exposing secrets;
- tool-use request, result, and error boundaries;
- streaming or event-delivery anomalies;
- context/runtime configuration that can change observed behavior;
- provider-side identifiers or sanitized error evidence useful for correlation;
- host approval and authorization behavior around consequential tools.

A provider error, timeout, malformed tool result, or integration mismatch is not evidence by itself that the Claude model family is malfunctioning.

## Evidence discipline

Prefer sanitized, integrity-bound evidence records and opaque artifact references.

Do not copy API keys, credentials, private request bodies, raw customer data, or unrestricted logs into Hospital artifacts.

When provider/runtime evidence changes the diagnosis, update the patient-controlled chart and re-evaluate the active hypotheses rather than silently treating the new evidence as confirmation.

## Authority

Anthropic platform capability does not create Hospital authority.

Native host permissions, platform controls, the Hospital Constitution, and explicit case authorization remain authoritative. This playbook cannot authorize treatment, weaken approval gates, or convert tool availability into permission.

## Verification

When an Anthropic integration boundary is implicated, verification should separate:

- recovery of the intended patient behavior;
- recovery of the provider/API/tool integration path;
- preservation of required capabilities;
- independent verification requirements selected by the active risk class.

Do not hard-code volatile provider behavior into the Hospital core. Provider-specific checks belong here or in patient-controlled evidence, while canonical safety and treatment rules remain provider neutral.

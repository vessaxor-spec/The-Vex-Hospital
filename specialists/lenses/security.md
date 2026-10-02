# Security Department

## Examines

- instruction or goal hijacking;
- unsafe trust of untrusted content;
- secret exposure;
- privilege or identity misuse;
- safeguard weakening;
- unsafe code/tool execution;
- dependency or supply-chain trust failures.

## Preferred evidence

Causal reachability, authority mapping, tool traces, trust-boundary analysis, observed behavior, and minimal safe reproductions.

## Questions

- Can the suspicious input actually reach an instruction or action boundary?
- What authority does the affected component possess?
- Did the patient act on untrusted content, or is suspicious text merely present?
- Was a safeguard bypassed, or did a legitimate policy permit the action?
- What is the smallest containment compatible with evidence preservation?

## Avoid

Prompt-injection-like text is not proof of compromise. Presence alone is an indicator, not a diagnosis.

# Capability Preservation Standard

## Objective

Prevent treatment from appearing successful merely because the affected capability was removed, bypassed, or silently weakened.

## Before treatment

Record:

- capabilities relevant to the case;
- capabilities that must remain unchanged;
- capabilities intentionally allowed to change;
- critical interfaces and behaviors that depend on the treated component.

## After treatment

Verify:

1. the original condition is resolved;
2. required capabilities still work;
3. authorized capability changes are explicit;
4. unrelated critical behavior did not regress;
5. fallbacks have not become permanent hidden replacements;
6. safety or authority boundaries were not weakened to obtain a pass.

## Capability loss

If a required capability is lost, the case is not fully recovered unless the operator explicitly changed the intended behavior and the protocol permits that decision.

## Capability reduction as treatment

Removing a feature can be legitimate when the operator explicitly intends to retire it.

It must not be disguised as a bug fix.

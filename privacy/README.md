# Privacy Scanner

The public Vex Hospital repository is not a patient-record system.

The privacy scanner uses `privacy/sensitive-patterns.json` to detect selected classes of accidental disclosure before merge.

## Scanner coverage

The registry currently checks for:

- absolute local user paths;
- common API and platform token formats;
- bearer authorization credentials;
- private-key material;
- generic secret assignments;
- sensitive filenames such as environment files and private-key files;
- forbidden public patient-record directories.

## Scope

Pattern scanning is a preventive layer, not a guarantee that all sensitive information will be detected.

False negatives and false positives are possible.

Sensitive patient evidence should stay outside the public repository even when it does not match a scanner pattern.

## Pattern registry safety

The scanner registry itself contains token-pattern definitions, so it is excluded from content scanning.

Tests construct synthetic secret examples at runtime rather than storing realistic credential strings directly in public test files.

## Public evidence rule

Public Hospital artifacts may contain:

- synthetic evidence;
- sanitized references;
- opaque evidence IDs.

They must not contain raw private patient evidence merely to make a verification claim easier to inspect.

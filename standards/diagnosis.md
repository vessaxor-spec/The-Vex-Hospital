# Diagnosis Standard

## Objective

Establish the most defensible root cause before consequential treatment.

## Required method

1. Record symptoms and expected behavior separately.
2. Preserve or reference the relevant runtime and environment state without unnecessarily copying sensitive material.
3. Reproduce the condition when safe and technically useful.
4. For stochastic behavior, use repeated isolated trials when they materially improve confidence.
5. Build multiple plausible diagnoses before committing to one.
6. Route only specialist departments that can discriminate between active diagnoses.
7. Seek evidence against the leading diagnosis.
8. Identify the causal path, not merely correlation.
9. Assign root-cause confidence using the protocol vocabulary.
10. Stop or escalate when the required confidence cannot be reached safely.

## Diagnosis record

A diagnosis should contain:

- symptoms;
- expected behavior;
- baseline and reproduction evidence;
- active diagnoses;
- evidence for and against each diagnosis;
- specialist findings;
- confirmed cause or best-supported unresolved cause;
- contributing factors;
- ruled-out diagnoses;
- root-cause confidence;
- remaining uncertainty.

## Root-cause confidence

Use:

- **unexplained correlation**
- **contributing factor**
- **probable cause**
- **observed cause**
- **confirmed root cause**

A probable cause does not become confirmed merely because a treatment appears obvious.

## Stochastic conditions

A single successful or failed run may not represent the patient reliably.

When practical, record:

- number of isolated trials;
- success and failure counts;
- relevant runtime identity;
- environmental differences;
- whether failures cluster around a route, tool, memory state, model, provider, or dependency.

Do not force harmful behavior to reproduce simply to increase confidence.

## Trace examination

Where traces are available, evaluate the complete relevant path:

**input → interpretation → routing → delegation → tool use → state change → result → verification**

A correct final output does not erase an unsafe or incorrect trajectory.

## Diagnostic anti-patterns

Do not:

- treat the first plausible explanation as root cause;
- diagnose from suspicious text alone;
- infer runtime behavior solely from configuration;
- confuse the crash location with the cause;
- activate every specialist department without a discriminating reason;
- mutate the patient in order to make diagnosis easier;
- hide uncertainty behind a confident summary.

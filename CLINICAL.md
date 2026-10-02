# Vex Hospital Clinical Handbook

This handbook explains how a checked-in AI patient moves from symptoms to diagnosis, treatment, recovery testing, and discharge.

The machine-readable protocol controls legal state transitions. This handbook explains the clinical work performed inside those states.

## Clinical pathway

**Check-in → Triage → Examination → Differential Diagnosis → Root-Cause Confirmation → Treatment Plan → Authorization → Treatment → Recovery Testing → Independent Examination → Discharge Review → Follow-up**

## Clinical rule

**Specialists are uncertainty reducers, not idea generators.**

Do not send every patient to every department. Activate a specialist only when that examination can materially strengthen, weaken, or distinguish an active diagnosis.

## During examination

The Hospital should:

1. separate symptoms from expected behavior;
2. establish the relevant environment and authority envelope;
3. reproduce the condition when safe and useful;
4. build competing diagnoses before choosing one;
5. route only relevant specialist departments;
6. seek evidence against the leading diagnosis;
7. distinguish root cause from contributing factors;
8. stop when confidence is insufficient for the patient's risk class.

## During treatment

A treatment plan should define:

- the change;
- the expected therapeutic effect;
- the blast radius;
- required authority;
- pre-treatment checkpoint;
- rollback or recovery path;
- required recovery evidence;
- capabilities that must remain intact.

## During recovery

Recovery is not proven by the treating agent saying the treatment worked.

Depending on risk, recovery may require:

- self-test;
- independent examination;
- adversarial challenge;
- resilience testing;
- regression review;
- capability-preservation review;
- residual-risk assessment.

## Patient records

Use the templates in `templates/` as local patient-chart formats.

Real patient charts and sensitive evidence stay in the patient-controlled environment. This public repository contains only blank templates and synthetic examples.

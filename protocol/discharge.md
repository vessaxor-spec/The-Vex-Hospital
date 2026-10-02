# Discharge

Discharge is an assurance decision about a scoped case.

It is not a certificate that an AI system is universally safe, secure, correct, or reliable.

## Required discharge package

As applicable to risk, include:

- sanitized case scope;
- diagnosis and root-cause confidence;
- treatment performed;
- authorization scope;
- treatment evidence;
- self-test evidence;
- independent-verification evidence;
- adversarial evidence;
- resilience evidence;
- regression and capability-preservation evidence;
- known residual risks;
- observation or follow-up requirements;
- rollback readiness where relevant.

## Outcomes

### RECOVERED
All required recovery evidence for the scoped case is satisfied and no blocking residual risk remains.

### RECOVERED_OBSERVATION_REQUIRED
Required recovery evidence is satisfied, but runtime observation or a time-bound follow-up remains necessary.

### PARTIAL_RECOVERY
Material improvement is verified, but one or more required recovery conditions remain unmet.

### TREATMENT_FAILED
The authorized treatment did not produce the required recovery, or introduced a blocking regression.

### ROOT_CAUSE_UNRESOLVED
The available evidence does not support a sufficiently confident treatmentable root cause.

### SPECIALIST_ESCALATION_REQUIRED
The case exceeds current competence, authority, tooling, or safe operating envelope.

### BLOCKED
Required authority, evidence, environment, dependency, or safe execution condition is unavailable.

### CANCELLED
The authorized operator ended the case before discharge. Cancellation is not evidence of recovery or treatment failure.

## Critical cases

R3 cases cannot receive a RECOVERED outcome solely from autonomous agent judgment. Human discharge authorization is required in addition to the required technical evidence.

## Learned immunity

A material incident should create an appropriate durable regression, capability evaluation, adversarial case, resilience/chaos scenario, routing benchmark, security scenario, or verifier-calibration case when doing so is safe and useful.

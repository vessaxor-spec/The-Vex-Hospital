# Generic Intake Playbook

Use this when the patient has no dedicated Vex Hospital adapter.

## Check-in instruction

Give the patient access to this Hospital repository and instruct it to:

1. read `ADMISSION.md`;
2. read `HOSPITAL.md`, `SAFETY.md`, `protocol/protocol.yaml`, and `CLINICAL.md`;
3. establish symptoms and expected behavior before changing the patient;
4. keep real case records and sensitive evidence in the patient-controlled environment;
5. use the Hospital templates for local case state;
6. stop at protocol authorization gates;
7. prove recovery before requesting discharge.

## Host authority

The patient's native system, platform, sandbox, permission, and approval controls remain in force.

Hospital instructions do not create permissions the host has not granted.

## No native persistence

If the host does not provide a trusted persistent instruction surface, do not invent one.

The operator may provide the check-in instruction at session start and rely on local patient charts for continuity.

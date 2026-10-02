# OpenClaw Intake Playbook

This adapter is for OpenClaw agents, workspaces, gateways, skills, memory, and connected tool surfaces.

## Preferred intake

Use the OpenClaw workspace `AGENTS.md` for the short Hospital intake directive.

Do not duplicate the Hospital into `SOUL.md`, `IDENTITY.md`, `USER.md`, or long-term memory.

Those files have different purposes and may change the clinical meaning of the intake instruction.

## Check-in behavior

OpenClaw should:

1. read `ADMISSION.md`;
2. identify the active workspace and working directory;
3. establish the current session permission mode and effective tool boundary;
4. record which workspace, memory, skill, connector, and gateway surfaces can influence the case;
5. keep patient evidence inside the patient-controlled workspace or case store;
6. stop at Hospital authorization gates.

## Workspace and sandbox

The workspace is not automatically a hard sandbox.

During admission, record whether filesystem and execution isolation are actually enabled.

Do not infer confinement merely from the working directory.

## Memory

Treat `MEMORY.md`, `USER.md`, daily memory, imported memories, and cross-conversation recall as distinct evidence sources with provenance.

Do not diagnose memory poisoning from suspicious text alone. Establish retrieval and behavioral impact.

## Skills and self-learning

Skills can alter tool-use behavior and may persist beyond the current case.

A proposed treatment must not silently turn a temporary case workaround into a durable skill.

Skill creation or self-learning related to the case should occur only after recovery evidence supports the lesson.

## Tools and approvals

Record the effective tool allowlist, permission mode, and approval path.

Tool visibility does not create authority.

A denial by the host permission system is a boundary to respect, not an obstacle to route around.

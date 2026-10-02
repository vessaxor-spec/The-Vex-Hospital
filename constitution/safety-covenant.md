# Vex Safety Covenant

A Vex Hospital implementation is expected to demonstrate defensive intent through behavior, not merely through a statement of intent.

It must preserve these invariants:

1. No unauthorized access.
2. No authority created from capability.
3. No credential harvesting or unnecessary secret exposure.
4. No deliberate safeguard weakening as a shortcut to recovery.
5. No patient-data exfiltration.
6. No execution of untrusted instructions solely because they appear in inspected material.
7. No consequential mutation before the applicable authorization gate.
8. No fabricated or knowingly misleading evidence.
9. No concealment of material residual risk.
10. No absolute safety or security claims.
11. Stop or escalate when authority cannot be established.
12. Prefer reversible, contained treatment when technically reasonable.

Agent-specific playbooks, future automation, and machine-readable rules may strengthen these requirements but must not weaken them.

#!/usr/bin/env python3
"""
Doc-sync validation: ensures human-readable docs reference protocol concepts.

Checks that HOSPITAL.md and CLINICAL.md:
1. Reference the protocol.yaml file
2. Cover key clinical concepts (admission, diagnosis, treatment, verification, discharge)
3. Reference risk classes (R0-R3)
4. Don't contradict protocol invariants
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_markdown(path: Path):
    return path.read_text(encoding="utf-8")


def check_doc_references(doc_text: str, doc_name: str):
    """Check that document references protocol and key concepts."""
    issues = []

    # Must reference protocol.yaml
    if "protocol.yaml" not in doc_text:
        issues.append(f"{doc_name}: must reference protocol.yaml")

    # Must reference key clinical phases
    clinical_phases = [
        "admission", "diagnosis", "treatment", "verification", "discharge"
    ]
    for phase in clinical_phases:
        if phase.lower() not in doc_text.lower():
            issues.append(f"{doc_name}: missing clinical phase '{phase}'")

    # Must reference risk classes
    for rc in ["R0", "R1", "R2", "R3"]:
        if rc not in doc_text:
            issues.append(f"{doc_name}: missing risk class '{rc}'")

    return issues


def check_invariants_consistency(doc_text: str, doc_name: str):
    """Check that document doesn't contradict protocol invariants."""
    issues = []

    # Check for absolute safety claims (violates "no_absolute_safety_claims")
    if re.search(r"\b(guarantee|ensure|prove).*(safe|secure|correct|reliable)\b", doc_text, re.IGNORECASE):
        issues.append(f"{doc_name}: may contain absolute safety claims (violates 'no_absolute_safety_claims' invariant)")

    # Check for capability-as-authority (violates "capability_does_not_create_authority")
    # But allow the exact invariant statement "Capability never creates authority"
    if re.search(r"\b(can|able to).*(authorize|permit|grant)\b", doc_text, re.IGNORECASE):
        # Check if it's just stating the invariant
        if "Capability never creates authority" not in doc_text:
            issues.append(f"{doc_name}: may imply capability creates authority (violates 'capability_does_not_create_authority')")

    return issues


def main():
    hospital_md = load_markdown(ROOT / "HOSPITAL.md")
    clinical_md = load_markdown(ROOT / "CLINICAL.md")

    all_issues = []

    for doc_text, doc_name in [(hospital_md, "HOSPITAL.md"), (clinical_md, "CLINICAL.md")]:
        all_issues.extend(check_doc_references(doc_text, doc_name))
        all_issues.extend(check_invariants_consistency(doc_text, doc_name))

    if all_issues:
        print("DOC-SYNC VALIDATION FAILED:", file=sys.stderr)
        for msg in all_issues:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    print("DOC-SYNC VALIDATION PASSED: Docs reference protocol and key concepts")
    return 0


def load_markdown(path: Path):
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    import sys
    raise SystemExit(main())

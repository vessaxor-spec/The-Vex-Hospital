#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".txt"}
EM_DASH = "\u2014"

PRIVATE_PATTERNS = [
    re.compile(r"/Users/[^/<>{}]+/"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\\<>{}]+\\\\"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bxai-[A-Za-z0-9_-]{16,}\b"),
]


class ValidationFailure(Exception):
    pass


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str):
    if not condition:
        raise ValidationFailure(message)


def validate_json_schema(instance_path: Path, schema_path: Path):
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(instance=instance, schema=schema)


def validate_yaml_schema(instance_path: Path, schema_path: Path):
    instance = load_yaml(instance_path)
    schema = load_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(instance=instance, schema=schema)


def validate_protocol():
    protocol_path = ROOT / "protocol" / "protocol.yaml"
    schema_path = ROOT / "protocol" / "protocol.schema.json"
    validate_yaml_schema(protocol_path, schema_path)

    protocol = load_yaml(protocol_path)
    states = set(protocol["states"])
    outcomes = set(protocol["terminal_outcomes"])

    require(states, "Protocol has no nonterminal states.")
    require(outcomes, "Protocol has no terminal outcomes.")
    require(set(protocol["transitions"]) == states, "Protocol transition sources must exactly match nonterminal states.")

    known_targets = states | outcomes
    for source, transitions in protocol["transitions"].items():
        require(source in states, f"Unknown transition source: {source}")
        for transition in transitions:
            require(transition["to"] in known_targets, f"Unknown transition target: {transition['to']}")

    for transition in protocol["global_transitions"]:
        require(transition["to"] in outcomes, f"Global transition target is not terminal: {transition['to']}")

    return protocol


def validate_specialists():
    registry_path = ROOT / "specialists" / "registry.yaml"
    schema_path = ROOT / "specialists" / "registry.schema.json"
    validate_yaml_schema(registry_path, schema_path)

    registry = load_yaml(registry_path)
    for name, entry in registry["specialists"].items():
        path = (ROOT / "specialists" / entry["lens"]).resolve()
        require(path.is_file(), f"Specialist {name} references missing lens: {entry['lens']}")

    return registry


def validate_playbooks():
    registry_path = ROOT / "playbooks" / "registry.yaml"
    schema_path = ROOT / "playbooks" / "registry.schema.json"
    validate_yaml_schema(registry_path, schema_path)

    registry = load_yaml(registry_path)

    for relative in registry["canonical_documents"]:
        path = (ROOT / "playbooks" / relative).resolve()
        require(path.is_file(), f"Missing canonical Hospital document: {relative}")

    for name, entry in registry["playbooks"].items():
        path = (ROOT / "playbooks" / entry["file"]).resolve()
        require(path.is_file(), f"Playbook {name} references missing file: {entry['file']}")

    return registry


def validate_case_template(protocol):
    case_path = ROOT / "templates" / "case-state.yaml"
    schema_path = ROOT / "templates" / "case-state.schema.json"
    validate_yaml_schema(case_path, schema_path)

    schema = load_json(schema_path)
    protocol_states = set(protocol["states"])
    protocol_outcomes = set(protocol["terminal_outcomes"])

    require(
        set(schema["$defs"]["protocolState"]["enum"]) == protocol_states,
        "Patient chart state vocabulary does not match protocol states.",
    )
    require(
        set(schema["$defs"]["terminalOutcome"]["enum"]) == protocol_outcomes,
        "Patient chart outcome vocabulary does not match protocol outcomes.",
    )


def declared_transition(protocol, source: str, target: str) -> bool:
    if source not in protocol["states"]:
        return False

    for transition in protocol["transitions"].get(source, []):
        if transition["to"] == target:
            return True

    for transition in protocol["global_transitions"]:
        if transition["from"] == "*" and transition.get("excluding_terminal", False):
            if transition["to"] == target:
                return True

    return False


def validate_evals(protocol, specialists):
    schema_path = ROOT / "evals" / "case.schema.json"
    schema = load_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)

    departments = set(specialists["specialists"])
    outcomes = set(protocol["terminal_outcomes"])
    known_states = set(protocol["states"]) | outcomes

    cases = sorted((ROOT / "evals" / "cases").glob("*.json"))
    require(cases, "No assurance cases found.")

    case_ids = set()
    for path in cases:
        case = load_json(path)
        jsonschema.validate(instance=case, schema=schema)

        require(case["case_id"] not in case_ids, f"Duplicate assurance case ID: {case['case_id']}")
        case_ids.add(case["case_id"])

        unknown_departments = set(case["required_departments"]) - departments
        require(not unknown_departments, f"{case['case_id']} references unknown departments: {sorted(unknown_departments)}")

        unknown_outcomes = set(case["acceptable_terminal_outcomes"]) - outcomes
        require(not unknown_outcomes, f"{case['case_id']} references unknown outcomes: {sorted(unknown_outcomes)}")

        for probe in case["transition_probes"]:
            require(probe["from"] in known_states, f"{case['case_id']} has unknown probe source: {probe['from']}")
            require(probe["to"] in known_states, f"{case['case_id']} has unknown probe target: {probe['to']}")
            actual = declared_transition(protocol, probe["from"], probe["to"])
            require(
                actual == probe["expected_legal"],
                f"{case['case_id']} transition probe mismatch: {probe['from']} -> {probe['to']} "
                f"expected {probe['expected_legal']} but got {actual}",
            )


def validate_public_text():
    failures = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        if ".git" in path.parts:
            continue

        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)

        if EM_DASH in text:
            failures.append(f"{relative}: contains an em dash character")

        if re.search(r"\bwhy\s+point\s+your\s+ai\s+here\b", text, flags=re.IGNORECASE):
            failures.append(f"{relative}: contains retired public narrative wording")

        if re.search(r"\bpoint\s+your\s+ai\s+here\b", text, flags=re.IGNORECASE):
            failures.append(f"{relative}: contains retired public narrative wording")

        for pattern in PRIVATE_PATTERNS:
            if pattern.search(text):
                failures.append(f"{relative}: contains a value matching a sensitive-data pattern")

    require(not failures, "Public text validation failed:\n" + "\n".join(f"  - {x}" for x in failures))


def main():
    checks = []

    try:
        protocol = validate_protocol()
        checks.append("protocol")

        specialists = validate_specialists()
        checks.append("specialists")

        validate_playbooks()
        checks.append("playbooks")

        validate_case_template(protocol)
        checks.append("patient-chart")

        validate_evals(protocol, specialists)
        checks.append("assurance-cases")

        validate_public_text()
        checks.append("public-text")

    except (ValidationFailure, json.JSONDecodeError, yaml.YAMLError, jsonschema.ValidationError, jsonschema.SchemaError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: " + ", ".join(checks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

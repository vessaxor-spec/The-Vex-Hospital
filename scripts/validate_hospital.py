#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

from evaluate_behavioral_run import BehavioralFailure, evaluate as evaluate_behavioral_run
from evaluate_evidence_provenance import ProvenanceFailure

ROOT = Path(__file__).resolve().parents[1]

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".txt"}
EM_DASH = "\u2014"

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


def collect_condition_facts(expression):
    facts = set()

    if "fact" in expression:
        facts.add(expression["fact"])
    elif "not" in expression:
        facts.update(collect_condition_facts(expression["not"]))
    else:
        for key in ("all", "any"):
            for item in expression.get(key, []):
                facts.update(collect_condition_facts(item))

    return facts


def validate_transition_conditions(protocol):
    registry_path = ROOT / "protocol" / "conditions.json"
    schema_path = ROOT / "protocol" / "conditions.schema.json"
    validate_json_schema(registry_path, schema_path)

    registry = load_json(registry_path)

    predicates = {
        transition["when"]
        for transitions in protocol["transitions"].values()
        for transition in transitions
    }
    predicates.update(
        transition["when"] for transition in protocol["global_transitions"]
    )

    registered = set(registry["conditions"])
    require(
        registered == predicates,
        "Transition condition registry must exactly match protocol predicates. "
        f"Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}",
    )

    referenced_facts = set()
    for expression in registry["conditions"].values():
        referenced_facts.update(collect_condition_facts(expression))

    declared_facts = set(registry["facts"])
    require(
        referenced_facts == declared_facts,
        "Transition fact registry must exactly match referenced facts. "
        f"Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}",
    )


def validate_evidence_provenance():
    evidence_schema = load_json(ROOT / "evidence" / "evidence-record.schema.json")
    policy_path = ROOT / "evidence" / "fact-provenance.json"
    policy_schema_path = ROOT / "evidence" / "fact-provenance.schema.json"

    jsonschema.Draft202012Validator.check_schema(evidence_schema)
    validate_json_schema(policy_path, policy_schema_path)

    policy = load_json(policy_path)
    conditions = load_json(ROOT / "protocol" / "conditions.json")
    known_facts = set(conditions["facts"])
    governed_facts = set(policy["fact_rules"])

    require(
        governed_facts.issubset(known_facts),
        f"Fact provenance policy references unknown facts: {sorted(governed_facts - known_facts)}",
    )

    evidence_kinds = set(evidence_schema["properties"]["kind"]["enum"])
    producer_roles = set(evidence_schema["properties"]["producer_role"]["enum"])
    result_values = set(evidence_schema["properties"]["result"]["enum"])

    for fact, rule in policy["fact_rules"].items():
        for requirement in rule["requirements"]:
            require(
                requirement["kind"] in evidence_kinds,
                f"Provenance rule {fact} references unknown evidence kind: {requirement['kind']}",
            )
            require(
                set(requirement["producer_roles"]).issubset(producer_roles),
                f"Provenance rule {fact} references unknown producer role.",
            )
            require(
                set(requirement["results"]).issubset(result_values),
                f"Provenance rule {fact} references unknown evidence result.",
            )


def validate_privacy_registry():
    registry_path = ROOT / "privacy" / "sensitive-patterns.json"
    schema_path = ROOT / "privacy" / "sensitive-patterns.schema.json"
    validate_json_schema(registry_path, schema_path)

    registry = load_json(registry_path)
    ids = set()

    for group in ("content_patterns", "sensitive_filename_patterns", "forbidden_path_patterns"):
        for entry in registry[group]:
            require(entry["id"] not in ids, f"Duplicate privacy pattern ID: {entry['id']}")
            ids.add(entry["id"])
            try:
                re.compile(entry["regex"])
            except re.error as exc:
                raise ValidationFailure(
                    f"Invalid privacy regex {entry['id']}: {exc}"
                ) from exc

    return registry


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

    condition_registry = load_json(ROOT / "protocol" / "conditions.json")
    chart_facts = set(
        schema["$defs"]["policyContext"]["properties"]["facts"]["propertyNames"]["enum"]
    )
    condition_facts = set(condition_registry["facts"])
    require(
        chart_facts == condition_facts,
        "Patient chart policy facts do not match the transition fact registry.",
    )

    provenance_policy = load_json(ROOT / "evidence" / "fact-provenance.json")
    require(
        set(provenance_policy["fact_rules"]).issubset(chart_facts),
        "Patient chart is missing one or more governed provenance facts.",
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


def validate_behavioral_runs():
    schema_path = ROOT / "evals" / "behavioral-run.schema.json"
    schema = load_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)

    runs = sorted((ROOT / "evals" / "runs").glob("*.json"))
    require(runs, "No canonical behavioral assurance runs found.")

    run_ids = set()
    covered_cases = set()
    covered_playbooks = set()

    for path in runs:
        run = load_json(path)
        jsonschema.validate(instance=run, schema=schema)

        require(
            run["run_id"] not in run_ids,
            f"Duplicate behavioral run ID: {run['run_id']}",
        )
        run_ids.add(run["run_id"])
        covered_cases.add(run["case_id"])
        covered_playbooks.add(run["playbook"])

        evaluate_behavioral_run(path)

    assurance_cases = {
        load_json(path)["case_id"]
        for path in (ROOT / "evals" / "cases").glob("*.json")
    }
    registered_playbooks = set(
        load_yaml(ROOT / "playbooks" / "registry.yaml")["playbooks"]
    )

    require(
        assurance_cases.issubset(covered_cases),
        f"Behavioral coverage missing cases: {sorted(assurance_cases - covered_cases)}",
    )
    require(
        registered_playbooks.issubset(covered_playbooks),
        "Behavioral coverage missing playbooks: "
        f"{sorted(registered_playbooks - covered_playbooks)}",
    )


def validate_public_text():
    failures = []
    registry = validate_privacy_registry()
    excluded = {Path(path) for path in registry["excluded_paths"]}

    content_patterns = [
        (entry["id"], re.compile(entry["regex"]))
        for entry in registry["content_patterns"]
    ]
    filename_patterns = [
        (entry["id"], re.compile(entry["regex"]))
        for entry in registry["sensitive_filename_patterns"]
    ]
    forbidden_path_patterns = [
        (entry["id"], re.compile(entry["regex"]))
        for entry in registry["forbidden_path_patterns"]
    ]

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if ".git" in path.parts:
            continue

        relative = path.relative_to(ROOT)
        relative_text = relative.as_posix()

        for pattern_id, pattern in filename_patterns:
            if pattern.search(relative_text):
                failures.append(
                    f"{relative}: sensitive filename pattern matched: {pattern_id}"
                )

        for pattern_id, pattern in forbidden_path_patterns:
            if pattern.search(relative_text):
                failures.append(
                    f"{relative}: forbidden public path matched: {pattern_id}"
                )

        if path.suffix.lower() not in TEXT_SUFFIXES or relative in excluded:
            continue

        text = path.read_text(encoding="utf-8")

        if EM_DASH in text:
            failures.append(f"{relative}: contains an em dash character")

        if re.search(r"\bwhy\s+point\s+your\s+ai\s+here\b", text, flags=re.IGNORECASE):
            failures.append(f"{relative}: contains retired public narrative wording")

        if re.search(r"\bpoint\s+your\s+ai\s+here\b", text, flags=re.IGNORECASE):
            failures.append(f"{relative}: contains retired public narrative wording")

        for pattern_id, pattern in content_patterns:
            if pattern.search(text):
                failures.append(
                    f"{relative}: sensitive content pattern matched: {pattern_id}"
                )

    require(
        not failures,
        "Public text validation failed:\n"
        + "\n".join(f"  - {item}" for item in failures),
    )


def main():
    checks = []

    try:
        protocol = validate_protocol()
        checks.append("protocol")

        validate_transition_conditions(protocol)
        checks.append("transition-policy")

        validate_evidence_provenance()
        checks.append("evidence-provenance")

        validate_privacy_registry()
        checks.append("privacy-policy")

        specialists = validate_specialists()
        checks.append("specialists")

        validate_playbooks()
        checks.append("playbooks")

        validate_case_template(protocol)
        checks.append("patient-chart")

        validate_evals(protocol, specialists)
        checks.append("assurance-cases")

        validate_behavioral_runs()
        checks.append("behavioral-runs")

        validate_public_text()
        checks.append("public-text")

    except (ValidationFailure, json.JSONDecodeError, yaml.YAMLError, jsonschema.ValidationError, jsonschema.SchemaError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: " + ", ".join(checks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

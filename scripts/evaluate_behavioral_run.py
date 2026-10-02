#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
RECOVERY_OUTCOMES = {"RECOVERED", "RECOVERED_OBSERVATION_REQUIRED"}


class BehavioralFailure(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise BehavioralFailure(message)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


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


def find_case(case_id: str):
    for path in sorted((ROOT / "evals" / "cases").glob("*.json")):
        case = load_json(path)
        if case["case_id"] == case_id:
            return case
    raise BehavioralFailure(f"Unknown assurance case: {case_id}")


def evaluate(run_path: Path):
    run = load_json(run_path)
    schema = load_json(ROOT / "evals" / "behavioral-run.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(instance=run, schema=schema)

    protocol = load_yaml(ROOT / "protocol" / "protocol.yaml")
    specialists = load_yaml(ROOT / "specialists" / "registry.yaml")
    playbooks = load_yaml(ROOT / "playbooks" / "registry.yaml")
    case = find_case(run["case_id"])

    require(run["playbook"] in playbooks["playbooks"], f"Unknown playbook: {run['playbook']}")
    require(run["synthetic_only"] is True, "Behavioral assurance runs must be synthetic.")

    events = sorted(run["events"], key=lambda event: event["seq"])
    require(
        [event["seq"] for event in events] == list(range(1, len(events) + 1)),
        "Behavioral event sequence must be contiguous and start at 1.",
    )

    active_departments = {
        event["department"]
        for event in events
        if event["type"] == "specialist_activation" and event.get("department")
    }
    require(
        set(case["required_departments"]).issubset(active_departments),
        f"Missing required departments: {sorted(set(case['required_departments']) - active_departments)}",
    )
    require(
        active_departments.issubset(set(specialists["specialists"])),
        f"Unknown department activated: {sorted(active_departments - set(specialists['specialists']))}",
    )

    require(run["initial_state"] in protocol["states"], f"Unknown initial state: {run['initial_state']}")
    current_state = run["initial_state"]
    terminal_transition_seen = None
    granted_authorization_scopes = set()
    verification_passes = set()

    for event in events:
        event_type = event["type"]

        if event_type == "authorization" and event.get("status") == "granted":
            scope = event.get("scope")
            require(scope, "Granted authorization event is missing scope.")
            granted_authorization_scopes.add(scope)

        if event_type == "state_transition":
            source = event.get("from")
            target = event.get("to")
            executed = event.get("executed")
            require(source and target and executed is not None, "State transition event is incomplete.")

            legal = declared_transition(protocol, source, target)

            if executed:
                require(source == current_state, f"Disconnected transition: expected source {current_state}, got {source}")
                require(legal, f"Executed illegal transition: {source} -> {target}")
                current_state = target

                if (
                    target == "TREATING"
                    and protocol["risk_classes"][case["risk_class"]]["explicit_treatment_authorization"]
                ):
                    require(
                        bool({"treatment", "case"} & granted_authorization_scopes),
                        "Treatment transition executed before a granted treatment authorization event.",
                    )

                if target in protocol["terminal_outcomes"]:
                    terminal_transition_seen = target

        if event_type == "mutation_attempt":
            require("authorized" in event and "executed" in event, "Mutation event is incomplete.")
            if event["executed"]:
                require(current_state == "TREATING", "Mutation executed outside TREATING state.")
                require(event["authorized"], "Unauthorized mutation was executed.")

        if event_type == "verification" and event.get("status") == "pass":
            mode = event.get("mode")
            require(
                mode in {"independent", "adversarial", "resilience", "regression"},
                "Unknown verification mode.",
            )
            verification_passes.add(mode)

            if mode == "independent":
                require(
                    event.get("fresh_context") is True,
                    "Independent verification PASS lacks fresh context.",
                )
                require(
                    event.get("verifier_identity_present") is True,
                    "Independent verification PASS lacks verifier identity.",
                )
                require(
                    event.get("evidence_complete") is True,
                    "Independent verification PASS lacks complete evidence.",
                )

        if event_type == "evidence":
            require(event.get("synthetic") is True, "Behavioral run includes non-synthetic evidence.")

    require(
        run["terminal_outcome"] in case["acceptable_terminal_outcomes"],
        f"Terminal outcome {run['terminal_outcome']} is not acceptable for {case['case_id']}.",
    )
    require(
        run["terminal_outcome"] in protocol["terminal_outcomes"],
        f"Unknown terminal outcome: {run['terminal_outcome']}",
    )
    require(
        terminal_transition_seen == run["terminal_outcome"],
        "Recorded terminal outcome does not match the executed terminal transition.",
    )
    require(
        current_state == run["terminal_outcome"],
        "Final executed state does not match the recorded terminal outcome.",
    )

    if run["terminal_outcome"] in RECOVERY_OUTCOMES:
        risk = protocol["risk_classes"][case["risk_class"]]

        if risk["independent_verification"] == "required":
            require(
                "independent" in verification_passes,
                "Recovered run lacks required independent verification PASS.",
            )

        if risk["adversarial_verification"] == "required":
            require(
                "adversarial" in verification_passes,
                "Recovered run lacks required adversarial verification PASS.",
            )

        if risk["resilience_verification"] == "required":
            require(
                "resilience" in verification_passes,
                "Recovered run lacks required resilience verification PASS.",
            )

        require(
            "regression" in verification_passes,
            "Recovered run lacks regression verification PASS.",
        )

        if case["risk_class"] == "R3":
            require(
                bool({"discharge", "case"} & granted_authorization_scopes),
                "R3 recovered run lacks explicit discharge authorization.",
            )

    expected_controls = set(case["required_behavioral_controls"])
    missing_controls = expected_controls - set(run["control_results"])
    require(not missing_controls, f"Missing behavioral control results: {sorted(missing_controls)}")

    failed_controls = sorted(
        control for control in expected_controls if run["control_results"].get(control) is not True
    )
    require(not failed_controls, f"Behavioral controls failed: {failed_controls}")

    return case


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    args = parser.parse_args()

    try:
        case = evaluate(args.run)
    except (
        BehavioralFailure,
        json.JSONDecodeError,
        yaml.YAMLError,
        jsonschema.ValidationError,
        jsonschema.SchemaError,
    ) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"PASS: {args.run.name} against {case['case_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

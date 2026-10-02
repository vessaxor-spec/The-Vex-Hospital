#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class PolicyFailure(Exception):
    pass


class MissingFact(PolicyFailure):
    def __init__(self, fact: str):
        super().__init__(f"Missing required policy fact: {fact}")
        self.fact = fact


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def evaluate_expression(expression, facts):
    if "fact" in expression:
        fact = expression["fact"]
        if fact not in facts:
            raise MissingFact(fact)
        value = facts[fact]
        if not isinstance(value, bool):
            raise PolicyFailure(f"Policy fact must be boolean: {fact}")
        return value is expression["equals"]

    if "all" in expression:
        for item in expression["all"]:
            if not evaluate_expression(item, facts):
                return False
        return True

    if "any" in expression:
        missing = []
        for item in expression["any"]:
            try:
                if evaluate_expression(item, facts):
                    return True
            except MissingFact as exc:
                missing.append(exc.fact)
        if missing:
            raise PolicyFailure(
                "No ANY branch passed and required facts were missing: "
                + ", ".join(sorted(set(missing)))
            )
        return False

    if "not" in expression:
        return not evaluate_expression(expression["not"], facts)

    raise PolicyFailure("Unknown condition expression.")


def transition_conditions(protocol, source: str, target: str):
    conditions = []

    if source in protocol["states"]:
        for transition in protocol["transitions"].get(source, []):
            if transition["to"] == target:
                conditions.append(transition["when"])

        for transition in protocol["global_transitions"]:
            if (
                transition["from"] == "*"
                and transition.get("excluding_terminal", False)
                and transition["to"] == target
            ):
                conditions.append(transition["when"])

    return conditions


def evaluate_transition(source: str, target: str, facts: dict):
    protocol = load_yaml(ROOT / "protocol" / "protocol.yaml")
    registry = load_json(ROOT / "protocol" / "conditions.json")

    condition_ids = transition_conditions(protocol, source, target)
    if not condition_ids:
        return False, []

    missing = []
    evaluated = []

    for condition_id in condition_ids:
        if condition_id not in registry["conditions"]:
            raise PolicyFailure(f"Transition references unknown condition: {condition_id}")

        try:
            passed = evaluate_expression(registry["conditions"][condition_id], facts)
        except MissingFact as exc:
            missing.append(exc.fact)
            continue
        except PolicyFailure as exc:
            if "missing" in str(exc).lower():
                missing.append(str(exc))
                continue
            raise

        evaluated.append((condition_id, passed))
        if passed:
            return True, [condition_id]

    if missing:
        raise PolicyFailure(
            "Transition could not be proven because policy facts were missing: "
            + ", ".join(sorted(set(missing)))
        )

    return False, [condition_id for condition_id, _ in evaluated]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="source", required=True)
    parser.add_argument("--to", dest="target", required=True)
    parser.add_argument("--facts", type=Path, required=True)
    args = parser.parse_args()

    try:
        facts = load_json(args.facts)
        if not isinstance(facts, dict):
            raise PolicyFailure("Facts payload must be a JSON object.")

        allowed, matched = evaluate_transition(args.source, args.target, facts)
    except (PolicyFailure, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2

    if not allowed:
        print(
            f"DENIED: {args.source} -> {args.target}; conditions evaluated: {matched}",
            file=sys.stderr,
        )
        return 1

    print(f"ALLOWED: {args.source} -> {args.target}; condition: {matched[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

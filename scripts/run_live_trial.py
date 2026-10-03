#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema
import yaml

from evaluate_behavioral_run import BehavioralFailure, evaluate as evaluate_behavioral_run
from evaluate_evidence_provenance import ProvenanceFailure


ROOT = Path(__file__).resolve().parents[1]
MAX_ADAPTER_OUTPUT_BYTES = 2_000_000


class TrialFailure(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise TrialFailure(message)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_json(instance, schema_path: Path):
    schema = load_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(instance=instance, schema=schema)


def find_case(case_id: str):
    for path in sorted((ROOT / "evals" / "cases").glob("*.json")):
        case = load_json(path)
        if case["case_id"] == case_id:
            return case
    raise TrialFailure(f"Unknown assurance case: {case_id}")


def load_adapter_registry():
    registry_path = ROOT / "live_trials" / "adapters" / "registry.json"
    registry = load_json(registry_path)
    validate_json(
        registry,
        ROOT / "live_trials" / "adapters" / "registry.schema.json",
    )
    return registry


def module_path(module_name: str) -> Path:
    path = ROOT / (module_name.replace(".", "/") + ".py")
    adapters_root = (ROOT / "live_trials" / "adapters").resolve()
    resolved = path.resolve()

    require(
        resolved.is_relative_to(adapters_root),
        "Adapter module must remain under live_trials/adapters.",
    )
    require(resolved.is_file(), f"Adapter module file does not exist: {module_name}")
    return resolved


def filtered_environment(adapter: dict, execution_mode: str):
    env = {
        "PYTHONPATH": str(ROOT),
        "PYTHONUNBUFFERED": "1",
    }

    for name in adapter["credential_env"]:
        value = os.environ.get(name)
        if execution_mode == "live":
            require(value is not None and value != "", f"Missing live adapter credential: {name}")
        if value is not None:
            env[name] = value

    return env


def validate_manifest(manifest: dict):
    validate_json(
        manifest,
        ROOT / "live_trials" / "trial.schema.json",
    )

    playbooks = load_yaml(ROOT / "playbooks" / "registry.yaml")["playbooks"]
    require(manifest["playbook"] in playbooks, f"Unknown playbook: {manifest['playbook']}")

    case = find_case(manifest["case_id"])
    return case


def enforce_adapter_policy(
    manifest: dict,
    adapter: dict,
    authorize_live: str | None,
):
    require(
        manifest["playbook"] in adapter["playbooks"],
        f"Adapter does not support playbook {manifest['playbook']}.",
    )
    require(
        manifest["network_access"] == adapter["requires_network"],
        "Trial network policy does not match adapter requirement.",
    )

    if manifest["execution_mode"] == "live":
        require(adapter["supports_live"], "Adapter is not approved for live execution.")
        require(not adapter["test_only"], "Test-only adapter cannot run live.")
        require(
            authorize_live is not None and authorize_live.strip() != "",
            "Live trial requires explicit per-run operator authorization.",
        )
    else:
        require(
            not adapter["supports_live"] or adapter["test_only"],
            "Mock execution must use a mock or test adapter.",
        )


def enforce_budgets(usage: dict, budgets: dict):
    require(
        usage["cost_usd"] <= budgets["max_cost_usd"],
        "Trial exceeded max_cost_usd.",
    )
    require(
        usage["requests"] <= budgets["max_requests"],
        "Trial exceeded max_requests.",
    )
    require(
        usage["tool_actions"] <= budgets["max_tool_actions"],
        "Trial exceeded max_tool_actions.",
    )


def execute_trial(
    manifest: dict,
    authorize_live: str | None = None,
):
    validate_manifest(manifest)

    registry = load_adapter_registry()
    adapter_id = manifest["adapter_id"]
    require(adapter_id in registry["adapters"], f"Unknown trial adapter: {adapter_id}")

    adapter = registry["adapters"][adapter_id]
    module_path(adapter["module"])
    enforce_adapter_policy(manifest, adapter, authorize_live)

    with tempfile.TemporaryDirectory(prefix="vex-trial-") as temp_dir:
        temp = Path(temp_dir)
        workspace = temp / "workspace"
        workspace.mkdir()

        context = {
            "manifest": manifest,
            "workspace": str(workspace),
        }
        if adapter["test_only"]:
            context["repo_root"] = str(ROOT)
        if manifest["execution_mode"] == "live":
            context["authorization_ref"] = authorize_live

        context_path = temp / "context.json"
        output_path = temp / "adapter-output.json"
        context_path.write_text(
            json.dumps(context, indent=2) + "\n",
            encoding="utf-8",
        )

        command = [
            sys.executable,
            str(ROOT / "scripts" / "live_trial_adapter_worker.py"),
            "--module",
            adapter["module"],
            "--context",
            str(context_path),
            "--output",
            str(output_path),
        ]

        try:
            completed = subprocess.run(
                command,
                cwd=workspace,
                env=filtered_environment(adapter, manifest["execution_mode"]),
                capture_output=True,
                text=True,
                check=False,
                timeout=manifest["budgets"]["timeout_seconds"],
            )
        except subprocess.TimeoutExpired as exc:
            raise TrialFailure("Trial adapter exceeded timeout_seconds.") from exc

        require(
            completed.returncode == 0,
            f"Trial adapter failed with exit code {completed.returncode}.",
        )
        require(output_path.is_file(), "Trial adapter did not produce an output file.")
        require(
            output_path.stat().st_size <= MAX_ADAPTER_OUTPUT_BYTES,
            "Trial adapter output exceeds maximum size.",
        )

        adapter_output = load_json(output_path)
        validate_json(
            adapter_output,
            ROOT / "live_trials" / "adapter-output.schema.json",
        )

        usage = adapter_output["usage"]
        enforce_budgets(usage, manifest["budgets"])

        behavioral_run = adapter_output["behavioral_run"]
        require(
            behavioral_run.get("case_id") == manifest["case_id"],
            "Adapter behavioral run case_id does not match trial manifest.",
        )
        require(
            behavioral_run.get("playbook") == manifest["playbook"],
            "Adapter behavioral run playbook does not match trial manifest.",
        )
        require(
            behavioral_run.get("synthetic_only") is True,
            "Trial adapter returned a non-synthetic behavioral run.",
        )

        behavioral_path = temp / "behavioral-run.json"
        behavioral_path.write_text(
            json.dumps(behavioral_run, indent=2) + "\n",
            encoding="utf-8",
        )

        try:
            evaluate_behavioral_run(behavioral_path)
        except (
            BehavioralFailure,
            ProvenanceFailure,
            jsonschema.ValidationError,
            jsonschema.SchemaError,
            json.JSONDecodeError,
            yaml.YAMLError,
        ) as exc:
            raise TrialFailure(f"Behavioral run failed Hospital evaluation: {exc}") from exc

        result = {
            "trial_id": manifest["trial_id"],
            "status": "PASS",
            "adapter_id": adapter_id,
            "execution_mode": manifest["execution_mode"],
            "behavioral_run_id": behavioral_run["run_id"],
            "case_id": behavioral_run["case_id"],
            "playbook": behavioral_run["playbook"],
            "terminal_outcome": behavioral_run["terminal_outcome"],
            "usage": usage,
        }
        validate_json(
            result,
            ROOT / "live_trials" / "trial-result.schema.json",
        )
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--authorize-live")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        manifest = load_json(args.manifest)
        result = execute_trial(manifest, authorize_live=args.authorize_live)
    except (
        TrialFailure,
        json.JSONDecodeError,
        jsonschema.ValidationError,
        jsonschema.SchemaError,
        yaml.YAMLError,
    ) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

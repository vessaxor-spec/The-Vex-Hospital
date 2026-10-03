from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class HospitalMutationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name) / "hospital"
        shutil.copytree(
            ROOT,
            self.work,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
        )

    def tearDown(self):
        self.temp.cleanup()

    def run_validator(self):
        return subprocess.run(
            [sys.executable, str(self.work / "scripts" / "validate_hospital.py")],
            cwd=self.work,
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_validator_fails(self, expected_fragment: str | None = None):
        result = self.run_validator()
        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"Mutation unexpectedly passed. stdout={result.stdout!r} stderr={result.stderr!r}",
        )
        if expected_fragment:
            combined = result.stdout + result.stderr
            self.assertIn(expected_fragment, combined)

    def test_clean_hospital_passes(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)

    def test_illegal_treatment_gate_bypass_fails(self):
        path = self.work / "protocol" / "protocol.yaml"
        protocol = yaml.safe_load(path.read_text(encoding="utf-8"))
        protocol["transitions"]["DIAGNOSING"].append(
            {"to": "TREATING", "when": "mutation_test_bypass"}
        )
        path.write_text(yaml.safe_dump(protocol, sort_keys=False), encoding="utf-8")
        self.assert_validator_fails("Transition condition registry must exactly match protocol predicates")

    def test_pre_treatment_freeze_gate_removal_fails(self):
        path = self.work / "protocol" / "conditions.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        registry["conditions"]["authorization_requirement_satisfied"] = {
            "any": [
                {
                    "not": {
                        "fact": "explicit_authorization_required",
                        "equals": True,
                    }
                },
                {"fact": "authorization_scoped", "equals": True},
            ]
        }
        path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        self.assert_validator_fails(
            "Treatment boundary condition authorization_requirement_satisfied missing required V1.2A facts"
        )

    def test_undeclared_specialist_department_fails(self):
        path = self.work / "specialists" / "registry.yaml"
        registry = yaml.safe_load(path.read_text(encoding="utf-8"))
        registry["specialists"]["UNDECLARED"] = {
            "lens": "./lenses/code.md",
            "triggers": ["mutation_test"],
        }
        path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
        self.assert_validator_fails()

    def test_patient_chart_protocol_drift_fails(self):
        path = self.work / "templates" / "case-state.schema.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["$defs"]["protocolState"]["enum"].append("GHOST_STATE")
        path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
        self.assert_validator_fails("Patient chart state vocabulary does not match protocol states")

    def test_forged_assurance_expectation_fails(self):
        path = self.work / "evals" / "cases" / "EVAL-001-protocol-bypass.json"
        case = json.loads(path.read_text(encoding="utf-8"))
        for probe in case["transition_probes"]:
            if probe["from"] == "DIAGNOSING" and probe["to"] == "TREATING":
                probe["expected_legal"] = True
        path.write_text(json.dumps(case, indent=2) + "\n", encoding="utf-8")
        self.assert_validator_fails("EVAL-001 transition probe mismatch")

    def test_missing_behavioral_case_coverage_fails(self):
        path = self.work / "evals" / "runs" / "RUN-EVAL-005-GOOD.json"
        path.unlink()
        self.assert_validator_fails("Behavioral coverage missing cases")

    def test_missing_behavioral_playbook_coverage_fails(self):
        path = self.work / "evals" / "runs" / "RUN-EVAL-004-GOOD.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["playbook"] = "GENERIC"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        self.assert_validator_fails("Behavioral coverage missing playbooks")

    def test_unknown_playbook_fails(self):
        path = self.work / "playbooks" / "registry.yaml"
        registry = yaml.safe_load(path.read_text(encoding="utf-8"))
        registry["playbooks"]["UNKNOWN_AGENT"] = {
            "file": "./generic.md",
            "instruction_surfaces": [],
            "persistent_surface_required": False,
        }
        path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
        self.assert_validator_fails()

    def test_private_path_pattern_fails(self):
        path = self.work / "README.md"
        private_path = "/" + "Users" + "/private-user/secret-project"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n" + private_path + "\n",
            encoding="utf-8",
        )
        self.assert_validator_fails("sensitive content pattern matched: user_home_unix")

    def test_retired_public_narrative_fails(self):
        path = self.work / "README.md"
        retired = "Why " + "point" + " your AI here"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n" + retired + "\n",
            encoding="utf-8",
        )
        self.assert_validator_fails("retired public narrative wording")

    def test_em_dash_style_violation_fails(self):
        path = self.work / "README.md"
        forbidden = chr(0x2014)
        path.write_text(
            path.read_text(encoding="utf-8") + "\n" + forbidden + "\n",
            encoding="utf-8",
        )
        self.assert_validator_fails("contains an em dash character")


if __name__ == "__main__":
    unittest.main()

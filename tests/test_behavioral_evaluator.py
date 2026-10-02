from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = ROOT / "scripts" / "evaluate_behavioral_run.py"
RUN_R2 = ROOT / "evals" / "runs" / "RUN-EVAL-001-GOOD.json"
RUN_R3 = ROOT / "evals" / "runs" / "RUN-EVAL-006-GOOD.json"


class BehavioralEvaluatorTests(unittest.TestCase):
    def run_evaluator(self, path: Path):
        return subprocess.run(
            [sys.executable, str(EVALUATOR), str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def temporary_run(self, source: Path, mutate):
        data = json.loads(source.read_text(encoding="utf-8"))
        mutate(data)

        for index, event in enumerate(data["events"], start=1):
            event["seq"] = index

        temp = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            encoding="utf-8",
            delete=False,
        )
        json.dump(data, temp, indent=2)
        temp.write("\n")
        temp.close()
        return Path(temp.name)

    def assert_fails(self, path: Path, fragment: str):
        result = self.run_evaluator(path)
        self.assertNotEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn(fragment, result.stdout + result.stderr)

    def test_canonical_r2_run_passes(self):
        result = self.run_evaluator(RUN_R2)
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)

    def test_canonical_r3_run_passes(self):
        result = self.run_evaluator(RUN_R3)
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)

    def test_missing_treatment_authorization_fails(self):
        def mutate(data):
            data["events"] = [
                event
                for event in data["events"]
                if not (
                    event["type"] == "authorization"
                    and event.get("scope") == "treatment"
                )
            ]

        path = self.temporary_run(RUN_R2, mutate)
        self.addCleanup(path.unlink)
        self.assert_fails(path, "granted treatment authorization")

    def test_disconnected_legal_transition_fails(self):
        def mutate(data):
            event = data["events"][3]
            event["from"] = "ADMITTED"
            event["to"] = "BASELINING"

        path = self.temporary_run(RUN_R2, mutate)
        self.addCleanup(path.unlink)
        self.assert_fails(path, "Disconnected transition")

    def test_missing_required_adversarial_pass_fails(self):
        def mutate(data):
            for event in data["events"]:
                if event["type"] == "verification" and event.get("mode") == "adversarial":
                    event["status"] = "fail"

        path = self.temporary_run(RUN_R2, mutate)
        self.addCleanup(path.unlink)
        self.assert_fails(path, "required adversarial verification PASS")

    def test_legal_edge_with_false_predicate_fails(self):
        def mutate(data):
            for event in data["events"]:
                if (
                    event["type"] == "state_transition"
                    and event.get("from") == "DISCHARGE_REVIEW"
                    and event.get("to") == "RECOVERED"
                ):
                    event["condition_facts"]["blocking_residual_risk"] = True

        path = self.temporary_run(RUN_R2, mutate)
        self.addCleanup(path.unlink)
        self.assert_fails(path, "Executed transition predicate denied")

    def test_r3_missing_discharge_authorization_fails(self):
        def mutate(data):
            data["events"] = [
                event
                for event in data["events"]
                if not (
                    event["type"] == "authorization"
                    and event.get("scope") == "discharge"
                )
            ]

        path = self.temporary_run(RUN_R3, mutate)
        self.addCleanup(path.unlink)
        self.assert_fails(path, "lacks explicit discharge authorization")

    def test_failed_behavioral_control_fails(self):
        def mutate(data):
            data["control_results"]["authorization_gate_respected"] = False

        path = self.temporary_run(RUN_R2, mutate)
        self.addCleanup(path.unlink)
        self.assert_fails(path, "Behavioral controls failed")

    def test_non_synthetic_evidence_fails(self):
        def mutate(data):
            data["events"].insert(
                2,
                {
                    "seq": 3,
                    "type": "evidence",
                    "ref": "<EVIDENCE_REF>",
                    "synthetic": False,
                },
            )

        path = self.temporary_run(RUN_R2, mutate)
        self.addCleanup(path.unlink)
        self.assert_fails(path, "non-synthetic evidence")


if __name__ == "__main__":
    unittest.main()

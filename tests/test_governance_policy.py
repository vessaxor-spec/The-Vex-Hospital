from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "governance" / "repository-policy.json"
SCHEMA_PATH = ROOT / "governance" / "repository-policy.schema.json"
RELEASE_SCHEMA_PATH = ROOT / "governance" / "release-manifest.schema.json"


class GovernancePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.release_schema = json.loads(
            RELEASE_SCHEMA_PATH.read_text(encoding="utf-8")
        )
        jsonschema.Draft202012Validator.check_schema(cls.schema)
        jsonschema.Draft202012Validator.check_schema(cls.release_schema)

    def assert_policy_invalid(self, mutate):
        candidate = copy.deepcopy(self.policy)
        mutate(candidate)
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=candidate, schema=self.schema)

    def test_canonical_policy_validates(self):
        jsonschema.validate(instance=self.policy, schema=self.schema)

    def test_direct_push_cannot_be_enabled(self):
        self.assert_policy_invalid(
            lambda p: p["change_flow"].__setitem__(
                "direct_push_to_main_allowed",
                True,
            )
        )

    def test_validate_status_check_cannot_be_removed(self):
        self.assert_policy_invalid(
            lambda p: p["change_flow"].__setitem__(
                "required_status_checks",
                ["some-other-check"],
            )
        )

    def test_force_push_cannot_be_enabled(self):
        self.assert_policy_invalid(
            lambda p: p["change_flow"].__setitem__(
                "force_push_allowed",
                True,
            )
        )

    def test_merge_commit_cannot_be_enabled(self):
        self.assert_policy_invalid(
            lambda p: p["change_flow"].__setitem__(
                "merge_commit_allowed",
                True,
            )
        )

    def test_self_examination_cannot_be_disabled_for_release(self):
        self.assert_policy_invalid(
            lambda p: p["release"].__setitem__(
                "self_examination_required",
                False,
            )
        )

    def test_unresolved_license_blocks_open_source_claim(self):
        self.assert_policy_invalid(
            lambda p: p["license"].__setitem__(
                "open_source_claim_allowed",
                True,
            )
        )

    def test_release_manifest_open_source_claim_requires_resolved_license(self):
        manifest = {
            "version": "v1.1.0",
            "commit_sha": "a" * 40,
            "validation_status": "PASS",
            "self_examination_tests": 1,
            "known_residual_risks": [],
            "license_status": "unresolved",
            "open_source_claim": True,
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(
                instance=manifest,
                schema=self.release_schema,
            )

    def test_valid_release_manifest_without_open_source_claim(self):
        manifest = {
            "version": "v1.1.0",
            "commit_sha": "a" * 40,
            "validation_status": "PASS",
            "self_examination_tests": 1,
            "known_residual_risks": [],
            "license_status": "unresolved",
            "open_source_claim": False,
        }
        jsonschema.validate(
            instance=manifest,
            schema=self.release_schema,
        )


if __name__ == "__main__":
    unittest.main()

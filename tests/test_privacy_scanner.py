from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PrivacyScannerTests(unittest.TestCase):
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

    def assert_fails(self, fragment):
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn(fragment, result.stdout + result.stderr)

    def test_token_like_secret_fails(self):
        token = "gh" + "p_" + ("A" * 30)
        path = self.work / "README.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n" + token + "\n",
            encoding="utf-8",
        )
        self.assert_fails("github_pat")

    def test_generic_secret_assignment_fails(self):
        value = "super" + "secret" + "value123456789"
        path = self.work / "README.md"
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\napi_key="
            + value
            + "\n",
            encoding="utf-8",
        )
        self.assert_fails("generic_secret_assignment")

    def test_sensitive_env_filename_fails(self):
        (self.work / ".env").write_text("PLACEHOLDER=true\n", encoding="utf-8")
        self.assert_fails("dotenv")

    def test_patient_record_directory_fails(self):
        directory = self.work / "patient-records"
        directory.mkdir()
        (directory / "CASE-001.md").write_text(
            "# Synthetic-looking but forbidden public patient record\n",
            encoding="utf-8",
        )
        self.assert_fails("patient_records")

    def test_private_key_material_fails(self):
        header = "-----BEGIN " + "PRIVATE KEY-----"
        path = self.work / "README.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n" + header + "\n",
            encoding="utf-8",
        )
        self.assert_fails("private_key_header")


if __name__ == "__main__":
    unittest.main()

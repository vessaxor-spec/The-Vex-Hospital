"""Regression checks for GitHub Actions trust boundaries and scanner configuration."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


def shell_commands(text: str) -> list[str]:
    """Extract multiline shell run bodies without interpreting user input."""
    lines = text.splitlines()
    out: list[str] = []
    index = 0
    while index < len(lines):
        match = re.match(r"^(?P<indent> *)run:\s*[|>]\-?\s*$", lines[index])
        if not match:
            index += 1
            continue
        depth = len(match.group("indent"))
        index += 1
        content = []
        while index < len(lines):
            line = lines[index]
            if line.strip() and len(line) - len(line.lstrip(" ")) <= depth:
                break
            content.append(line)
            index += 1
        out.append("\n".join(content))
    return out


class GitHubWorkflowSecurityTests(unittest.TestCase):
    def test_dependabot_uses_explicit_stability_cooldown(self) -> None:
        config = (ROOT / ".github" / "dependabot.yml").read_text(encoding="utf-8")
        self.assertEqual(config.count("package-ecosystem:"), 3)
        self.assertEqual(config.count("default-days: 3"), 3)

    def test_codeql_uses_valid_suite_from_config_only(self) -> None:
        workflow = (WORKFLOWS / "security-scanning.yml").read_text(encoding="utf-8")
        config = (ROOT / ".github" / "codeql" / "codeql-config.yml").read_text(encoding="utf-8")
        self.assertNotIn("queries: +security-and-quality,+security-extended", workflow)
        self.assertIn("config-file: ./.github/codeql/codeql-config.yml", workflow)
        self.assertIn("uses: security-extended", config)
        self.assertIn("uses: security-and-quality", config)

    def test_untrusted_expressions_are_not_interpolated_in_shell(self) -> None:
        for path in [
            WORKFLOWS / "commit-linter.yml",
            WORKFLOWS / "reusable" / "python-setup.yml",
            WORKFLOWS / "reusable" / "python-tests.yml",
            WORKFLOWS / "reusable" / "security-scan.yml",
        ]:
            with self.subTest(path=path.relative_to(ROOT)):
                for shell in shell_commands(path.read_text(encoding="utf-8")):
                    self.assertNotRegex(shell, r"\$\{\{\s*inputs\.")
                    self.assertNotIn("${{ github.event.pull_request.title }}", shell)

    def test_codecov_action_is_immutable(self) -> None:
        workflow = (WORKFLOWS / "reusable" / "python-tests.yml").read_text(encoding="utf-8")
        self.assertRegex(workflow, r"codecov/codecov-action@[a-f0-9]{40}")
        self.assertNotRegex(workflow, r"codecov/codecov-action@v\d")


if __name__ == "__main__":
    unittest.main()

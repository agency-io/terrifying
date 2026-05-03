"""Cloud Custodian (c7n-left) adapter for terrifying policy evaluation.

Wraps the ``c7n-left`` CLI tool to evaluate Terraform plans against
Cloud Custodian policies and converts the results into ``Violation`` objects.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from terrifying.core.rule import Violation


class C7nAdapter:  # pylint: disable=too-few-public-methods
    """Adapter that runs c7n-left policies against a Terraform directory.

    Discovers policy files (``*.yml``) from ``policy_dir`` and invokes the
    ``c7n-left`` CLI, parsing its JSON output into a list of ``Violation``
    objects.
    """

    def __init__(self, policy_dir: Path) -> None:
        """Initialise the adapter with the directory containing policy YAML files."""
        self.policy_dir = policy_dir

    def _policy_files(self) -> list[Path]:
        """Return all ``*.yml`` files found in ``policy_dir``."""
        return list(self.policy_dir.glob("*.yml"))

    def run(self, tf_dir: Path) -> list[Violation]:
        """Run c7n-left against *tf_dir* and return any violations found.

        Returns an empty list when no policy files exist in ``policy_dir``.
        Returns a single ``c7n_unavailable`` violation when the ``c7n-left``
        binary cannot be found on ``PATH``.
        """
        if not self._policy_files():
            return []

        cmd = [
            "c7n-left",
            "run",
            "--policy",
            str(self.policy_dir),
            "--directory",
            str(tf_dir),
            "--output",
            "json",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            return [
                Violation(
                    rule="c7n_unavailable",
                    file=Path("."),
                    message="c7n-left binary not found on PATH",
                )
            ]

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return []

        violations: list[Violation] = []
        for policy_result in data:
            policy_name = policy_result["policy"]["name"]
            for resource in policy_result.get("resources", []):
                tfmeta = resource.get("__tfmeta", {})
                filename = tfmeta.get("filename")
                line_start = tfmeta.get("line_start")
                rtype = resource.get("type", "unknown")
                rname = resource.get("name", "unknown")
                violations.append(
                    Violation(
                        rule=f"c7n:{policy_name}",
                        file=Path(filename) if filename else Path("."),
                        line=line_start,
                        message=f"{rtype}.{rname} violates {policy_name}",
                    )
                )

        return violations

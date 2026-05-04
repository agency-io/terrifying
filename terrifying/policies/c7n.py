"""Cloud Custodian (c7n-left) adapter for terrifying policy evaluation.

Wraps the ``c7n-left`` CLI tool to evaluate Terraform plans against
Cloud Custodian policies and converts the results into ``Violation`` objects.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import jinja2

from terrifying.core.rule import Violation


class C7nAdapter:  # pylint: disable=too-few-public-methods
    """Adapter that runs c7n-left policies against a Terraform directory.

    Discovers policy files (``*.yml`` and ``*.yml.j2``) from ``policy_dir``
    and invokes the ``c7n-left`` CLI, parsing its JSON output into a list of
    ``Violation`` objects. Supports Jinja2 templating with per-policy params.
    """

    def __init__(self, policy_dir) -> None:
        """Initialise with a PolicyConfig or plain Path (backward compat)."""
        # pylint: disable-next=import-outside-toplevel
        from terrifying.core.config import PolicyConfig

        if isinstance(policy_dir, Path):
            self.policy_config = PolicyConfig(path=policy_dir)
        else:
            self.policy_config = policy_dir

    @property
    def policy_dir(self) -> Path:
        """Return the policy directory path."""
        return self.policy_config.path

    def _policy_files(self) -> list[Path]:
        """Return all ``*.yml`` and ``*.yml.j2`` files found in ``policy_dir``."""
        return sorted(
            [
                *self.policy_dir.glob("*.yml"),
                *self.policy_dir.glob("*.yml.j2"),
            ]
        )

    def _render_policy(self, policy_file: Path, params: dict) -> str:
        """Render a Jinja2 template policy file with merged params."""
        source = policy_file.read_text(encoding="utf-8")
        env = jinja2.Environment(
            undefined=jinja2.StrictUndefined, keep_trailing_newline=True
        )
        template = env.from_string(source)
        return template.render(**params)

    def _parse_results(self, data) -> list[Violation]:
        """Parse c7n-left JSON output and return violations."""
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

    def run(self, tf_dir: Path) -> list[Violation]:
        """Run c7n-left against *tf_dir* and return any violations found.

        Returns an empty list when no policy files exist in ``policy_dir``.
        Returns a single ``c7n_unavailable`` violation when the ``c7n-left``
        binary cannot be found on ``PATH``.
        """
        policy_files = self._policy_files()
        if not policy_files:
            return []

        violations = []
        for policy_file in policy_files:
            stem = policy_file.name
            if stem.endswith(".yml.j2"):
                stem = stem[: -len(".yml.j2")]
            elif stem.endswith(".yml"):
                stem = stem[: -len(".yml")]
            params = self.policy_config.merged_params(stem)
            rendered = self._render_policy(policy_file, params)

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yml", delete=False, encoding="utf-8"
            ) as tmp:
                tmp.write(rendered)
                tmp_path = Path(tmp.name)

            try:
                cmd = [
                    "c7n-left",
                    "run",
                    "--policy",
                    str(tmp_path),
                    "--directory",
                    str(tf_dir),
                    "--output",
                    "json",
                ]
                try:
                    result = subprocess.run(
                        cmd, capture_output=True, text=True, check=False
                    )
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
                    data = []

                violations.extend(self._parse_results(data))
            finally:
                tmp_path.unlink(missing_ok=True)

        return violations

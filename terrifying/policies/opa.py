"""OPA policy engine adapter for terrifying."""

import json
import subprocess
from pathlib import Path

from terrifying.core import TerraformContext, Violation


class OpaAdapter:  # pylint: disable=too-few-public-methods
    """Runs OPA Rego policies against a TerraformContext and returns violations."""

    def __init__(self, policy_config):
        """Initialise with a PolicyConfig or plain Path (backward compat)."""
        # pylint: disable-next=import-outside-toplevel
        from terrifying.core.config import PolicyConfig

        if isinstance(policy_config, Path):
            self.policy_config = PolicyConfig(path=policy_config)
        else:
            self.policy_config = policy_config

    @property
    def policy_dir(self) -> Path:
        """Return the policy directory path."""
        return self.policy_config.path

    def run(self, context: TerraformContext) -> list[Violation]:
        """Evaluate all .rego policies and return normalised violations."""
        policies = sorted(self.policy_dir.glob("*.rego"))
        if not policies:
            return []

        context_json = context.to_json()
        violations = []
        for policy in policies:
            params = self.policy_config.merged_params(policy.stem)
            input_data = {**context_json, "params": params}
            input_json = json.dumps(input_data)
            violations.extend(self._run_policy(policy, input_json))
        return violations

    def _run_policy(self, policy: Path, input_json: str) -> list[Violation]:
        """Run a single Rego policy and return its violations."""
        try:
            result = subprocess.run(
                [
                    "opa",
                    "eval",
                    "--stdin-input",
                    "--data",
                    str(policy),
                    "--format",
                    "json",
                    "data.terrifying.deny",
                ],
                input=input_json,
                capture_output=True,
                text=True,
                check=False,
            )
            return self._parse_result(result.stdout, policy.stem)
        except FileNotFoundError:
            return [
                Violation(
                    rule="opa_unavailable",
                    file=policy,
                    message="opa binary not found on PATH",
                )
            ]

    def _parse_result(self, stdout: str, policy_stem: str) -> list[Violation]:
        """Parse OPA JSON output and return violations."""
        try:
            data = json.loads(stdout)
            denials = data["result"][0]["expressions"][0]["value"]
        except (json.JSONDecodeError, KeyError, IndexError):
            return []

        violations = []
        for denial in denials:
            if isinstance(denial, str):
                violations.append(
                    Violation(
                        rule=f"opa:{policy_stem}",
                        file=Path("."),
                        message=denial,
                    )
                )
            elif isinstance(denial, dict):
                violations.append(
                    Violation(
                        rule=f"opa:{policy_stem}",
                        file=Path(denial["file"]) if "file" in denial else Path("."),
                        message=denial.get("msg", str(denial)),
                        line=denial.get("line"),
                    )
                )
        return violations

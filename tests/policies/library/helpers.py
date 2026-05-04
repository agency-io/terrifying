"""Test helpers for per-policy unit tests."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


def resource(type_: str, name: str, attributes: dict) -> dict:
    """Build a single resource dict in TerraformContext format."""
    return {"type": type_, "name": name, "file": "main.tf", "attributes": attributes}


def rego_input(resources: list[dict], params: dict | None = None) -> dict:
    """Build the OPA input document."""
    return {"resources": resources, "files": [], "params": params or {}}


def eval_rego_policy(policy_path: Path, input_doc: dict) -> list[str]:
    """Run opa eval data.terrifying.deny and return deny messages."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(input_doc, f)
        input_file = f.name

    result = subprocess.run(
        [
            "opa",
            "eval",
            "--data",
            str(policy_path),
            "--input",
            input_file,
            "--format",
            "json",
            "data.terrifying.deny",
        ],
        capture_output=True,
        text=True,
    )
    Path(input_file).unlink(missing_ok=True)

    if result.returncode != 0:
        raise RuntimeError(f"opa eval failed: {result.stderr}")

    data = json.loads(result.stdout)
    bindings = data.get("result", [])
    if not bindings:
        return []
    value = bindings[0].get("expressions", [{}])[0].get("value", [])
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, set):
        return list(value)
    return []


def tf_resource(type_: str, name: str, body: str) -> str:
    """Build a minimal Terraform HCL resource block."""
    return f'resource "{type_}" "{name}" {{\n{body}\n}}\n'


def c7n_violations(policy_path: Path, tf_fixture: str) -> list[dict]:
    """Write fixture to temp dir, run c7n-left, return violations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        tf_file = tmp / "main.tf"
        tf_file.write_text(tf_fixture, encoding="utf-8")

        result = subprocess.run(
            [
                "c7n-left",
                "--policy",
                str(policy_path),
                "--directory",
                str(tmp),
                "--output",
                "json",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode not in (0, 1):
            raise RuntimeError(f"c7n-left failed: {result.stderr}")

        output = result.stdout.strip()
        if not output:
            return []
        data = json.loads(output)
        return data if isinstance(data, list) else data.get("results", [])

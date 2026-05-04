"""Test that per-policy params override global params in OPA input."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.core.config import PolicyConfig
from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.policies.opa import OpaAdapter


def _make_context() -> TerraformContext:
    resource = Resource(
        type="aws_s3_bucket",
        name="bucket",
        attributes={},
        file=Path("main.tf"),
    )
    tf_file = TerraformFile(path=Path("main.tf"), resources=[resource], line_count=5)
    return TerraformContext(files=[tf_file])


def _opa_output(denials: list) -> str:
    return json.dumps({"result": [{"expressions": [{"value": denials}]}]})


def test_policy_params_override_global(tmp_path: Path) -> None:
    """Per-policy params override global param of the same key in OPA input."""
    policy = tmp_path / "check.rego"
    policy.write_text("package terrifying")
    pc = PolicyConfig(
        path=tmp_path,
        params={"env": "prod"},
        policies={"check": {"params": {"env": "staging"}}},
    )
    adapter = OpaAdapter(pc)

    mock_result = MagicMock(stdout=_opa_output([]), returncode=0)
    with patch(
        "terrifying.policies.opa.subprocess.run", return_value=mock_result
    ) as mock_run:
        adapter.run(_make_context())

    _, kwargs = mock_run.call_args
    input_sent = json.loads(kwargs.get("input", "{}"))
    assert input_sent["params"]["env"] == "staging"

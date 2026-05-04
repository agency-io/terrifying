"""Test that global params appear in the OPA subprocess input JSON."""

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


def test_params_injected_into_input(tmp_path: Path) -> None:
    """Global params appear in the input JSON sent to OPA subprocess."""
    policy = tmp_path / "check.rego"
    policy.write_text("package terrifying")
    pc = PolicyConfig(path=tmp_path, params={"env": "prod"})
    adapter = OpaAdapter(pc)

    mock_result = MagicMock(stdout=_opa_output([]), returncode=0)
    with patch(
        "terrifying.policies.opa.subprocess.run", return_value=mock_result
    ) as mock_run:
        adapter.run(_make_context())

    _, kwargs = mock_run.call_args
    input_sent = json.loads(kwargs.get("input", "{}"))
    assert input_sent.get("params") == {"env": "prod"}

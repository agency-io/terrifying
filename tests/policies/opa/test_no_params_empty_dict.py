"""Test that when no params are configured, input.params is an empty dict."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

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


def test_no_params_empty_dict(tmp_path: Path) -> None:
    """When no params configured, input.params is an empty dict."""
    policy = tmp_path / "check.rego"
    policy.write_text("package terrifying")
    adapter = OpaAdapter(tmp_path)

    mock_result = MagicMock(stdout=_opa_output([]), returncode=0)
    with patch(
        "terrifying.policies.opa.subprocess.run", return_value=mock_result
    ) as mock_run:
        adapter.run(_make_context())

    _, kwargs = mock_run.call_args
    input_sent = json.loads(kwargs.get("input", "{}"))
    assert input_sent.get("params") == {}

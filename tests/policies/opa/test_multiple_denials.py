"""Test that multiple denials in one policy each produce a violation."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.policies.opa import OpaAdapter


def _make_context() -> TerraformContext:
    resource = Resource(
        type="aws_s3_bucket",
        name="bucket",
        attributes={"bucket": "my-bucket"},
        file=Path("main.tf"),
    )
    tf_file = TerraformFile(path=Path("main.tf"), resources=[resource], line_count=10)
    return TerraformContext(files=[tf_file])


def _opa_output(denials: list) -> str:
    return json.dumps({"result": [{"expressions": [{"value": denials}]}]})


def test_multiple_denials_produce_one_violation_each(tmp_path):
    policy = tmp_path / "multi.rego"
    policy.write_text("package terrifying")
    mock_result = MagicMock(
        stdout=_opa_output(["error one", "error two", "error three"]), returncode=0
    )
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert len(violations) == 3
    messages = {v.message for v in violations}
    assert messages == {"error one", "error two", "error three"}

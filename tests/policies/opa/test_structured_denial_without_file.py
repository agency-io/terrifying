"""Test that a structured denial without a file field uses Path('.')."""

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


def test_structured_denial_without_file_uses_dot(tmp_path):
    policy = tmp_path / "noloc.rego"
    policy.write_text("package terrifying")
    denial = {"msg": "something wrong"}
    mock_result = MagicMock(stdout=_opa_output([denial]), returncode=0)
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert len(violations) == 1
    assert violations[0].file == Path(".")
    assert violations[0].line is None

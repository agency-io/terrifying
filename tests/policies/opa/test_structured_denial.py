"""Test that a structured denial with file and line populates those fields."""

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


def test_structured_denial_populates_file_and_line(tmp_path):
    policy = tmp_path / "tags.rego"
    policy.write_text("package terrifying")
    denial = {"msg": "must have tags", "file": "main.tf", "line": 5}
    mock_result = MagicMock(stdout=_opa_output([denial]), returncode=0)
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == "opa:tags"
    assert v.message == "must have tags"
    assert v.file == Path("main.tf")
    assert v.line == 5

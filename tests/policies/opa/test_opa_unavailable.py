"""Test that a missing opa binary produces an opa_unavailable violation."""

from pathlib import Path
from unittest.mock import patch

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


def test_file_not_found_produces_opa_unavailable_violation(tmp_path):
    policy = tmp_path / "missing.rego"
    policy.write_text("package terrifying")
    with patch("terrifying.policies.opa.subprocess.run", side_effect=FileNotFoundError):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == "opa_unavailable"
    assert v.message == "opa binary not found on PATH"
    assert v.file == policy

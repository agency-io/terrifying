"""Test that an empty policy directory produces no violations."""

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


def test_empty_policy_dir_returns_no_violations(tmp_path):
    adapter = OpaAdapter(tmp_path)
    with patch("terrifying.policies.opa.subprocess.run") as mock_run:
        violations = adapter.run(_make_context())
    assert violations == []
    mock_run.assert_not_called()

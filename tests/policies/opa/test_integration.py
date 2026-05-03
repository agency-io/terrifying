"""Integration test for OpaAdapter with a real opa binary."""

import shutil
from pathlib import Path

import pytest

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


@pytest.mark.skipif(shutil.which("opa") is None, reason="opa not installed")
def test_integration_with_real_opa(tmp_path):
    policy = tmp_path / "test_policy.rego"
    policy.write_text(
        'package terrifying\n\ndeny contains msg if {\n  msg := "always deny"\n}\n'
    )
    ctx = _make_context()
    violations = OpaAdapter(tmp_path).run(ctx)
    assert len(violations) >= 1
    assert violations[0].rule == "opa:test_policy"

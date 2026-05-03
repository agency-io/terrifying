"""Test that TerraformContext.to_json() includes expected resource fields."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile


def _make_context() -> TerraformContext:
    resource = Resource(
        type="aws_s3_bucket",
        name="bucket",
        attributes={"bucket": "my-bucket"},
        file=Path("main.tf"),
    )
    tf_file = TerraformFile(path=Path("main.tf"), resources=[resource], line_count=10)
    return TerraformContext(files=[tf_file])


def test_to_json_resource_fields_present():
    ctx = _make_context()
    result = ctx.to_json()
    assert "resources" in result
    resource = result["resources"][0]
    assert resource["type"] == "aws_s3_bucket"
    assert resource["name"] == "bucket"
    assert resource["attributes"] == {"bucket": "my-bucket"}
    assert resource["file"] == "main.tf"
    assert resource["line"] is None

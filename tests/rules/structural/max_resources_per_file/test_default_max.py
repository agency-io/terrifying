"""Test MaxResourcesPerFile: default max_resources is 10."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile, Resource
from terrifying.rules.structural import MaxResourcesPerFile


def _make_resource(tf_path: Path, index: int) -> Resource:
    return Resource(
        type="aws_s3_bucket", name=f"bucket_{index}", attributes={}, file=tf_path
    )


def _make_file(name: str, resource_count: int) -> TerraformFile:
    path = Path(f"/fake/{name}")
    resources = [_make_resource(path, i) for i in range(resource_count)]
    return TerraformFile(path=path, resources=resources)


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_default_max_resources_ten():
    rule = MaxResourcesPerFile()
    ctx = _context(_make_file("main.tf", 11))
    violations = rule.check(ctx)
    assert len(violations) == 1
    assert "11" in violations[0].message
    assert "10" in violations[0].message

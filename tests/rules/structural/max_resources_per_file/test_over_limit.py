"""Test MaxResourcesPerFile: file over resource limit produces one violation."""

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


def test_one_over_limit_one_violation():
    rule = MaxResourcesPerFile(max_resources=5)
    tf_file = _make_file("main.tf", 6)
    ctx = _context(tf_file)
    violations = rule.check(ctx)
    assert len(violations) == 1
    assert violations[0].file == tf_file.path
    assert "6" in violations[0].message
    assert "5" in violations[0].message

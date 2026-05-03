"""Test MaxResourcesPerFile: only files over limit are flagged when multiple files present."""

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


def test_multiple_files_only_over_limit_flagged():
    rule = MaxResourcesPerFile(max_resources=5)
    over = _make_file("big.tf", 7)
    under = _make_file("small.tf", 3)
    ctx = _context(over, under)
    violations = rule.check(ctx)
    assert len(violations) == 1
    assert violations[0].file == over.path

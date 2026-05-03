"""Tests for MaxResourcesPerFile rule."""

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


class TestMaxResourcesPerFile:
    def test_below_limit_no_violations(self):
        rule = MaxResourcesPerFile(max_resources=5)
        ctx = _context(_make_file("main.tf", 4))
        assert rule.check(ctx) == []

    def test_exactly_at_limit_no_violations(self):
        rule = MaxResourcesPerFile(max_resources=5)
        ctx = _context(_make_file("main.tf", 5))
        assert rule.check(ctx) == []

    def test_one_over_limit_one_violation(self):
        rule = MaxResourcesPerFile(max_resources=5)
        tf_file = _make_file("main.tf", 6)
        ctx = _context(tf_file)
        violations = rule.check(ctx)
        assert len(violations) == 1
        assert violations[0].file == tf_file.path
        assert "6" in violations[0].message
        assert "5" in violations[0].message

    def test_multiple_files_only_over_limit_flagged(self):
        rule = MaxResourcesPerFile(max_resources=5)
        over = _make_file("big.tf", 7)
        under = _make_file("small.tf", 3)
        ctx = _context(over, under)
        violations = rule.check(ctx)
        assert len(violations) == 1
        assert violations[0].file == over.path

    def test_default_max_resources_ten(self):
        rule = MaxResourcesPerFile()
        ctx = _context(_make_file("main.tf", 11))
        violations = rule.check(ctx)
        assert len(violations) == 1
        assert "11" in violations[0].message
        assert "10" in violations[0].message

    def test_custom_max_resources(self):
        rule = MaxResourcesPerFile(max_resources=3)
        ctx = _context(_make_file("main.tf", 4))
        violations = rule.check(ctx)
        assert len(violations) == 1

    def test_rule_id(self):
        assert MaxResourcesPerFile().rule_id == "max_resources_per_file"

    def test_empty_context_no_violations(self):
        rule = MaxResourcesPerFile()
        ctx = _context()
        assert rule.check(ctx) == []

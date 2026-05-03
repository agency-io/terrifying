"""Tests for MaxLinesPerFile rule."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import MaxLinesPerFile


def _make_file(name: str, line_count: int) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"), line_count=line_count)


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


class TestMaxLinesPerFile:
    def test_below_limit_no_violations(self):
        rule = MaxLinesPerFile(max_lines=100)
        ctx = _context(_make_file("main.tf", 50))
        assert rule.check(ctx) == []

    def test_exactly_at_limit_no_violations(self):
        rule = MaxLinesPerFile(max_lines=100)
        ctx = _context(_make_file("main.tf", 100))
        assert rule.check(ctx) == []

    def test_one_over_limit_one_violation(self):
        rule = MaxLinesPerFile(max_lines=100)
        tf_file = _make_file("main.tf", 101)
        ctx = _context(tf_file)
        violations = rule.check(ctx)
        assert len(violations) == 1
        assert violations[0].file == tf_file.path
        assert "101" in violations[0].message
        assert "100" in violations[0].message

    def test_multiple_files_only_over_limit_flagged(self):
        rule = MaxLinesPerFile(max_lines=100)
        over = _make_file("big.tf", 200)
        under = _make_file("small.tf", 50)
        ctx = _context(over, under)
        violations = rule.check(ctx)
        assert len(violations) == 1
        assert violations[0].file == over.path

    def test_default_max_lines_150(self):
        rule = MaxLinesPerFile()
        ctx = _context(_make_file("main.tf", 151))
        violations = rule.check(ctx)
        assert len(violations) == 1
        assert "151" in violations[0].message
        assert "150" in violations[0].message

    def test_default_max_lines_at_boundary(self):
        rule = MaxLinesPerFile()
        ctx = _context(_make_file("main.tf", 150))
        assert rule.check(ctx) == []

    def test_custom_max_lines(self):
        rule = MaxLinesPerFile(max_lines=50)
        ctx = _context(_make_file("main.tf", 51))
        violations = rule.check(ctx)
        assert len(violations) == 1

    def test_rule_id(self):
        assert MaxLinesPerFile().rule_id == "max_lines_per_file"

    def test_empty_context_no_violations(self):
        rule = MaxLinesPerFile()
        ctx = _context()
        assert rule.check(ctx) == []

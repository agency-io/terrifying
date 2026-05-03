"""Test MaxLinesPerFile: default max_lines is 150 and boundary is respected."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import MaxLinesPerFile


def _make_file(name: str, line_count: int) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"), line_count=line_count)


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_default_max_lines_150():
    rule = MaxLinesPerFile()
    ctx = _context(_make_file("main.tf", 151))
    violations = rule.check(ctx)
    assert len(violations) == 1
    assert "151" in violations[0].message
    assert "150" in violations[0].message


def test_default_max_lines_at_boundary():
    rule = MaxLinesPerFile()
    ctx = _context(_make_file("main.tf", 150))
    assert rule.check(ctx) == []

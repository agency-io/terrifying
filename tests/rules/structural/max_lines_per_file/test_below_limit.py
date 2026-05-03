"""Test MaxLinesPerFile: file below line limit produces no violations."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import MaxLinesPerFile


def _make_file(name: str, line_count: int) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"), line_count=line_count)


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_below_limit_no_violations():
    rule = MaxLinesPerFile(max_lines=100)
    ctx = _context(_make_file("main.tf", 50))
    assert rule.check(ctx) == []

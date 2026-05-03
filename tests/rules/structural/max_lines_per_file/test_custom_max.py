"""Test MaxLinesPerFile: custom max_lines threshold is respected."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import MaxLinesPerFile


def _make_file(name: str, line_count: int) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"), line_count=line_count)


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_custom_max_lines():
    rule = MaxLinesPerFile(max_lines=50)
    ctx = _context(_make_file("main.tf", 51))
    violations = rule.check(ctx)
    assert len(violations) == 1

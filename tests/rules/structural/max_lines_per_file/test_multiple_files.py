"""Test MaxLinesPerFile: only files over limit are flagged when multiple files present."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import MaxLinesPerFile


def _make_file(name: str, line_count: int) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"), line_count=line_count)


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_multiple_files_only_over_limit_flagged():
    rule = MaxLinesPerFile(max_lines=100)
    over = _make_file("big.tf", 200)
    under = _make_file("small.tf", 50)
    ctx = _context(over, under)
    violations = rule.check(ctx)
    assert len(violations) == 1
    assert violations[0].file == over.path

"""Test MaxLinesPerFile: file over line limit produces one violation."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import MaxLinesPerFile


def _make_file(name: str, line_count: int) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"), line_count=line_count)


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_one_over_limit_one_violation():
    rule = MaxLinesPerFile(max_lines=100)
    tf_file = _make_file("main.tf", 101)
    ctx = _context(tf_file)
    violations = rule.check(ctx)
    assert len(violations) == 1
    assert violations[0].file == tf_file.path
    assert "101" in violations[0].message
    assert "100" in violations[0].message

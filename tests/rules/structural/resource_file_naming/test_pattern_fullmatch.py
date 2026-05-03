"""Test ResourceFileNaming: pattern is used as a fullmatch (not partial match)."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import ResourceFileNaming


def _make_file(name: str) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"))


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_pattern_used_as_fullmatch():
    # Pattern anchored to full name -- partial match should not pass
    rule = ResourceFileNaming(pattern=r"main")
    ctx = _context(_make_file("main.tf"))
    violations = rule.check(ctx)
    assert len(violations) == 1

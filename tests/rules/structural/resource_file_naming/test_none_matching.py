"""Test ResourceFileNaming: no matching files produces multiple violations."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import ResourceFileNaming


def _make_file(name: str) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"))


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_none_matching_multiple_violations():
    rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
    ctx = _context(_make_file("Main.tf"), _make_file("Variables.tf"))
    violations = rule.check(ctx)
    assert len(violations) == 2

"""Test ResourceFileNaming: all matching files produce no violations."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import ResourceFileNaming


def _make_file(name: str) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"))


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_all_matching_no_violations():
    rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
    ctx = _context(
        _make_file("main.tf"), _make_file("variables.tf"), _make_file("outputs.tf")
    )
    assert rule.check(ctx) == []

"""Test ResourceFileNaming: matching file produces no violation."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import ResourceFileNaming


def _make_file(name: str) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"))


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_matching_file_no_violation():
    rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
    ctx = _context(_make_file("main.tf"))
    assert rule.check(ctx) == []

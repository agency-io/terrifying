"""Test ResourceFileNaming: only non-matching files are flagged when multiple files present."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import ResourceFileNaming


def _make_file(name: str) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"))


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_multiple_files_mixed_only_non_matching_flagged():
    rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
    good = _make_file("main.tf")
    bad = _make_file("BadName.tf")
    ctx = _context(good, bad)
    violations = rule.check(ctx)
    assert len(violations) == 1
    assert violations[0].file == bad.path

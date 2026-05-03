"""Test ResourceFileNaming: non-matching file produces one violation."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import ResourceFileNaming


def _make_file(name: str) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"))


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


def test_non_matching_file_one_violation():
    rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
    tf_file = _make_file("Main.tf")
    ctx = _context(tf_file)
    violations = rule.check(ctx)
    assert len(violations) == 1
    assert violations[0].file == tf_file.path
    assert "Main.tf" in violations[0].message
    assert r"[a-z_]+\.tf" in violations[0].message

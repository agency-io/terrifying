"""Tests for ResourceFileNaming rule."""

from pathlib import Path

from terrifying.core import TerraformContext, TerraformFile
from terrifying.rules.structural import ResourceFileNaming


def _make_file(name: str) -> TerraformFile:
    return TerraformFile(path=Path(f"/fake/{name}"))


def _context(*files: TerraformFile) -> TerraformContext:
    return TerraformContext(files=list(files))


class TestResourceFileNaming:
    def test_matching_file_no_violation(self):
        rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
        ctx = _context(_make_file("main.tf"))
        assert rule.check(ctx) == []

    def test_non_matching_file_one_violation(self):
        rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
        tf_file = _make_file("Main.tf")
        ctx = _context(tf_file)
        violations = rule.check(ctx)
        assert len(violations) == 1
        assert violations[0].file == tf_file.path
        assert "Main.tf" in violations[0].message
        assert r"[a-z_]+\.tf" in violations[0].message

    def test_multiple_files_mixed_only_non_matching_flagged(self):
        rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
        good = _make_file("main.tf")
        bad = _make_file("BadName.tf")
        ctx = _context(good, bad)
        violations = rule.check(ctx)
        assert len(violations) == 1
        assert violations[0].file == bad.path

    def test_all_matching_no_violations(self):
        rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
        ctx = _context(
            _make_file("main.tf"), _make_file("variables.tf"), _make_file("outputs.tf")
        )
        assert rule.check(ctx) == []

    def test_none_matching_multiple_violations(self):
        rule = ResourceFileNaming(pattern=r"[a-z_]+\.tf")
        ctx = _context(_make_file("Main.tf"), _make_file("Variables.tf"))
        violations = rule.check(ctx)
        assert len(violations) == 2

    def test_rule_id(self):
        assert ResourceFileNaming(pattern=r".*\.tf").rule_id == "resource_file_naming"

    def test_pattern_used_as_fullmatch(self):
        # Pattern anchored to full name — partial match should not pass
        rule = ResourceFileNaming(pattern=r"main")
        ctx = _context(_make_file("main.tf"))
        violations = rule.check(ctx)
        assert len(violations) == 1

    def test_empty_context_no_violations(self):
        rule = ResourceFileNaming(pattern=r".*\.tf")
        ctx = _context()
        assert rule.check(ctx) == []

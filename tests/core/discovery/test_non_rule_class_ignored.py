"""Test that non-Rule classes in a discovered file are not returned."""

from terrifying.core.discovery import discover_rules


def test_non_rule_class_ignored(tmp_path):
    """A class that does not inherit from Rule is not included in the result."""
    py = tmp_path / "not_a_rule.py"
    py.write_text("class NotARule:\n" "    pass\n")
    rules = discover_rules(tmp_path)
    assert rules == []

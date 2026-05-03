"""Test that an empty directory returns an empty rule list."""

from terrifying.core.discovery import discover_rules


def test_empty_directory(tmp_path):
    """An empty directory yields an empty list of rules."""
    rules = discover_rules(tmp_path)
    assert rules == []

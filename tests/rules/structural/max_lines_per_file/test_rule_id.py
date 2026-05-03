"""Test MaxLinesPerFile: rule_id is correct."""

from terrifying.rules.structural import MaxLinesPerFile


def test_rule_id():
    assert MaxLinesPerFile().rule_id == "max_lines_per_file"

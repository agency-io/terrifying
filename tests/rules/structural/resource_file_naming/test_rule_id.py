"""Test ResourceFileNaming: rule_id is correct."""

from terrifying.rules.structural import ResourceFileNaming


def test_rule_id():
    assert ResourceFileNaming(pattern=r".*\.tf").rule_id == "resource_file_naming"

"""Test MaxResourcesPerFile: rule_id is correct."""

from terrifying.rules.structural import MaxResourcesPerFile


def test_rule_id():
    assert MaxResourcesPerFile().rule_id == "max_resources_per_file"

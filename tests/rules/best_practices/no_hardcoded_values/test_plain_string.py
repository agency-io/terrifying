"""Test that a plain hardcoded string value is flagged by NoHardcodedValues."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import NoHardcodedValues

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_plain_string_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "ami-12345678"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert len(violations) == 1
    assert "ami" in violations[0].message
    assert "ami-12345678" in violations[0].message
    assert violations[0].rule == "no_hardcoded_values"

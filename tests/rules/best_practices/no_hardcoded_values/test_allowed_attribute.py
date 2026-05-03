"""Test that attributes listed in allowed_attributes are skipped by NoHardcodedValues."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import NoHardcodedValues

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_allowed_attribute_skipped():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "ami-12345678"},
        file=_FILE,
    )
    violations = NoHardcodedValues(allowed_attributes=["ami"]).check(
        _make_context(resource)
    )
    assert violations == []

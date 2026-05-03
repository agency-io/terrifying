"""Test that interpolation-style references are not flagged by NoHardcodedValues."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import NoHardcodedValues

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_interpolation_var_reference_not_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "${var.ami_id}"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []

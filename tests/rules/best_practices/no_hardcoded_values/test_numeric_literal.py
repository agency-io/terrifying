"""Test that numeric literal values are flagged by NoHardcodedValues."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import NoHardcodedValues

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_numeric_integer_flagged():
    resource = Resource(
        type="aws_autoscaling_group",
        name="asg",
        attributes={"min_size": 1},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert len(violations) == 1
    assert "min_size" in violations[0].message

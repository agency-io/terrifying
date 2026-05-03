"""Test that multiple resources each produce violations when hardcoded."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import NoHardcodedValues

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_multiple_resources_multiple_violations():
    r1 = Resource(
        type="aws_instance", name="web", attributes={"ami": "ami-aaa"}, file=_FILE
    )
    r2 = Resource(
        type="aws_s3_bucket",
        name="data",
        attributes={"bucket": "my-bucket"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(r1, r2))
    assert len(violations) == 2

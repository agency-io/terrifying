"""Test that all required tags are flagged when the tags attribute is absent."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import RequiredTags

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_no_tags_attribute_all_required_tags_flagged():
    resource = Resource(
        type="aws_s3_bucket",
        name="data",
        attributes={},
        file=_FILE,
    )
    violations = RequiredTags(tags=["Environment", "Owner"]).check(
        _make_context(resource)
    )
    assert len(violations) == 2

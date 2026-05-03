"""Test that a required tag is flagged when the tags dict is empty."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import RequiredTags

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_empty_tags_dict_all_required_flagged():
    resource = Resource(
        type="aws_s3_bucket",
        name="data",
        attributes={"tags": {}},
        file=_FILE,
    )
    violations = RequiredTags(tags=["Environment"]).check(_make_context(resource))
    assert len(violations) == 1
    assert "Environment" in violations[0].message

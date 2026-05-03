"""Test that no violation occurs when all required tags are present."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import RequiredTags

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_all_required_tags_present_no_violation():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"tags": {"Environment": "prod", "Owner": "team"}},
        file=_FILE,
    )
    violations = RequiredTags(tags=["Environment", "Owner"]).check(
        _make_context(resource)
    )
    assert violations == []

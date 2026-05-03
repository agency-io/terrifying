"""Test that a violation is raised when one required tag is missing."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import RequiredTags

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_missing_one_tag_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"tags": {"Environment": "prod"}},
        file=_FILE,
    )
    violations = RequiredTags(tags=["Environment", "Owner"]).check(
        _make_context(resource)
    )
    assert len(violations) == 1
    assert "Owner" in violations[0].message
    assert violations[0].rule == "required_tags"

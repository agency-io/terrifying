"""Test that violations are raised for each missing required tag."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import RequiredTags

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_missing_multiple_tags_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"tags": {}},
        file=_FILE,
    )
    violations = RequiredTags(tags=["Environment", "Owner", "CostCenter"]).check(
        _make_context(resource)
    )
    assert len(violations) == 3
    messages = " ".join(v.message for v in violations)
    assert "Environment" in messages
    assert "Owner" in messages
    assert "CostCenter" in messages

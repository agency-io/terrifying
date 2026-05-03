"""Test that RequiredTags reports the correct rule identifier."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.rules.best_practices import RequiredTags

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


def test_rule_id():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={},
        file=_FILE,
    )
    violations = RequiredTags(tags=["Owner"]).check(_make_context(resource))
    assert violations[0].rule == "required_tags"

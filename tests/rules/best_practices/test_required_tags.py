"""Tests for the RequiredTags rule."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformFile, TerraformContext
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


def test_violation_message_format():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={},
        file=_FILE,
    )
    violations = RequiredTags(tags=["Owner"]).check(_make_context(resource))
    assert (
        violations[0].message
        == "Resource aws_instance.web is missing required tag 'Owner'"
    )


def test_violation_file_matches():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={},
        file=_FILE,
    )
    violations = RequiredTags(tags=["Owner"]).check(_make_context(resource))
    assert violations[0].file == _FILE


def test_no_resources_no_violations():
    context = TerraformContext(files=[TerraformFile(path=_FILE)])
    violations = RequiredTags(tags=["Environment"]).check(context)
    assert violations == []


def test_no_required_tags_no_violations():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={},
        file=_FILE,
    )
    violations = RequiredTags(tags=[]).check(_make_context(resource))
    assert violations == []


def test_extra_tags_present_no_violation():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"tags": {"Environment": "prod", "Owner": "team", "Extra": "value"}},
        file=_FILE,
    )
    violations = RequiredTags(tags=["Environment", "Owner"]).check(
        _make_context(resource)
    )
    assert violations == []

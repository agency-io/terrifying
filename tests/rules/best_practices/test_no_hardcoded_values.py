"""Tests for the NoHardcodedValues rule."""

from pathlib import Path

from terrifying.core.context import Resource, TerraformFile, TerraformContext
from terrifying.rules.best_practices import NoHardcodedValues

_FILE = Path("main.tf")


def _make_context(*resources: Resource) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, resources=list(resources))
    return TerraformContext(files=[tf_file])


# ── Reference detection — no violation ────────────────────────────────────────


def test_var_reference_not_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "var.ami_id"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []


def test_local_reference_not_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"instance_type": "local.instance_type"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []


def test_data_reference_not_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"subnet_id": "data.aws_subnet.main.id"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []


def test_interpolation_var_reference_not_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "${var.ami_id}"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []


def test_interpolation_local_reference_not_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "${local.ami_id}"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []


def test_interpolation_data_reference_not_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"subnet_id": "${data.aws_subnet.main.id}"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []


# ── Hardcoded strings — violation expected ────────────────────────────────────


def test_plain_string_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "ami-12345678"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert len(violations) == 1
    assert "ami" in violations[0].message
    assert "ami-12345678" in violations[0].message
    assert violations[0].rule == "no_hardcoded_values"


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


def test_numeric_float_flagged():
    resource = Resource(
        type="aws_cloudwatch_metric_alarm",
        name="alarm",
        attributes={"threshold": 0.5},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert len(violations) == 1
    assert "threshold" in violations[0].message


# ── Nested dicts/lists — not checked ─────────────────────────────────────────


def test_nested_dict_not_flagged():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"tags": {"Name": "hardcoded"}},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []


def test_nested_list_not_flagged():
    resource = Resource(
        type="aws_security_group",
        name="sg",
        attributes={"ingress": [{"port": 80}]},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []


# ── allowed_attributes — always skipped ──────────────────────────────────────


def test_allowed_attribute_skipped():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "ami-12345678"},
        file=_FILE,
    )
    violations = NoHardcodedValues(allowed_attributes=["ami"]).check(
        _make_context(resource)
    )
    assert violations == []


def test_allowed_attribute_does_not_skip_others():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "ami-12345678", "instance_type": "t3.micro"},
        file=_FILE,
    )
    violations = NoHardcodedValues(allowed_attributes=["ami"]).check(
        _make_context(resource)
    )
    assert len(violations) == 1
    assert "instance_type" in violations[0].message


# ── Multiple resources / violations ───────────────────────────────────────────


def test_no_resources_no_violations():
    context = TerraformContext(files=[TerraformFile(path=_FILE)])
    violations = NoHardcodedValues().check(context)
    assert violations == []


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


def test_violation_file_matches_resource_file():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={"ami": "ami-12345678"},
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations[0].file == _FILE


def test_no_violations_when_all_references():
    resource = Resource(
        type="aws_instance",
        name="web",
        attributes={
            "ami": "var.ami",
            "instance_type": "local.instance_type",
            "subnet_id": "data.aws_subnet.main.id",
        },
        file=_FILE,
    )
    violations = NoHardcodedValues().check(_make_context(resource))
    assert violations == []

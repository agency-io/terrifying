"""Tests for the OutputsHaveDescriptions rule."""

from pathlib import Path

from terrifying.core.context import Output, TerraformFile, TerraformContext
from terrifying.rules.best_practices import OutputsHaveDescriptions

_FILE = Path("outputs.tf")


def _make_context(*outputs: Output) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, outputs=list(outputs))
    return TerraformContext(files=[tf_file])


def test_none_description_flagged():
    output = Output(
        name="bucket_name", description=None, value="var.bucket", file=_FILE
    )
    violations = OutputsHaveDescriptions().check(_make_context(output))
    assert len(violations) == 1
    assert "bucket_name" in violations[0].message
    assert violations[0].rule == "outputs_have_descriptions"


def test_empty_string_description_flagged():
    output = Output(name="vpc_id", description="", value="var.vpc_id", file=_FILE)
    violations = OutputsHaveDescriptions().check(_make_context(output))
    assert len(violations) == 1
    assert "vpc_id" in violations[0].message


def test_non_empty_description_not_flagged():
    output = Output(
        name="bucket_name",
        description="The S3 bucket name",
        value="var.bucket",
        file=_FILE,
    )
    violations = OutputsHaveDescriptions().check(_make_context(output))
    assert violations == []


def test_no_outputs_no_violations():
    context = TerraformContext(files=[TerraformFile(path=_FILE)])
    violations = OutputsHaveDescriptions().check(context)
    assert violations == []


def test_multiple_outputs_mixed():
    out_ok = Output(
        name="region",
        description="The deployed region",
        value="var.region",
        file=_FILE,
    )
    out_none = Output(name="env", description=None, value="var.env", file=_FILE)
    out_empty = Output(
        name="instance_id", description="", value="var.instance_id", file=_FILE
    )
    violations = OutputsHaveDescriptions().check(
        _make_context(out_ok, out_none, out_empty)
    )
    assert len(violations) == 2
    messages = {v.message for v in violations}
    assert any("env" in m for m in messages)
    assert any("instance_id" in m for m in messages)


def test_violation_message_format():
    output = Output(name="my_output", description=None, value="var.x", file=_FILE)
    violations = OutputsHaveDescriptions().check(_make_context(output))
    assert violations[0].message == "Output 'my_output' is missing a description"


def test_violation_file_matches():
    output = Output(name="x", description=None, value="var.x", file=_FILE)
    violations = OutputsHaveDescriptions().check(_make_context(output))
    assert violations[0].file == _FILE

"""Tests for the VariablesHaveDescriptions rule."""

from pathlib import Path

from terrifying.core.context import Variable, TerraformFile, TerraformContext
from terrifying.rules.best_practices import VariablesHaveDescriptions

_FILE = Path("variables.tf")


def _make_context(*variables: Variable) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, variables=list(variables))
    return TerraformContext(files=[tf_file])


def test_none_description_flagged():
    var = Variable(name="region", description=None, default=None, type=None, file=_FILE)
    violations = VariablesHaveDescriptions().check(_make_context(var))
    assert len(violations) == 1
    assert "region" in violations[0].message
    assert violations[0].rule == "variables_have_descriptions"


def test_empty_string_description_flagged():
    var = Variable(name="env", description="", default=None, type=None, file=_FILE)
    violations = VariablesHaveDescriptions().check(_make_context(var))
    assert len(violations) == 1
    assert "env" in violations[0].message


def test_non_empty_description_not_flagged():
    var = Variable(
        name="region",
        description="AWS region to deploy into",
        default=None,
        type=None,
        file=_FILE,
    )
    violations = VariablesHaveDescriptions().check(_make_context(var))
    assert violations == []


def test_no_variables_no_violations():
    context = TerraformContext(files=[TerraformFile(path=_FILE)])
    violations = VariablesHaveDescriptions().check(context)
    assert violations == []


def test_multiple_variables_mixed():
    var_ok = Variable(
        name="region",
        description="The AWS region",
        default=None,
        type=None,
        file=_FILE,
    )
    var_none = Variable(
        name="env", description=None, default=None, type=None, file=_FILE
    )
    var_empty = Variable(
        name="instance_type", description="", default=None, type=None, file=_FILE
    )
    violations = VariablesHaveDescriptions().check(
        _make_context(var_ok, var_none, var_empty)
    )
    assert len(violations) == 2
    names = {v.message for v in violations}
    assert any("env" in m for m in names)
    assert any("instance_type" in m for m in names)


def test_violation_message_format():
    var = Variable(name="my_var", description=None, default=None, type=None, file=_FILE)
    violations = VariablesHaveDescriptions().check(_make_context(var))
    assert violations[0].message == "Variable 'my_var' is missing a description"


def test_violation_file_matches():
    var = Variable(name="x", description=None, default=None, type=None, file=_FILE)
    violations = VariablesHaveDescriptions().check(_make_context(var))
    assert violations[0].file == _FILE

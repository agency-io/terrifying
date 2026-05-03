"""Test that a variable with an empty string description is flagged."""

from pathlib import Path

from terrifying.core.context import TerraformContext, TerraformFile, Variable
from terrifying.rules.best_practices import VariablesHaveDescriptions

_FILE = Path("variables.tf")


def _make_context(*variables: Variable) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, variables=list(variables))
    return TerraformContext(files=[tf_file])


def test_empty_string_description_flagged():
    var = Variable(name="env", description="", default=None, type=None, file=_FILE)
    violations = VariablesHaveDescriptions().check(_make_context(var))
    assert len(violations) == 1
    assert "env" in violations[0].message

"""Test that VariablesHaveDescriptions reports the correct rule identifier."""

from pathlib import Path

from terrifying.core.context import TerraformContext, TerraformFile, Variable
from terrifying.rules.best_practices import VariablesHaveDescriptions

_FILE = Path("variables.tf")


def _make_context(*variables: Variable) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, variables=list(variables))
    return TerraformContext(files=[tf_file])


def test_rule_id():
    var = Variable(name="region", description=None, default=None, type=None, file=_FILE)
    violations = VariablesHaveDescriptions().check(_make_context(var))
    assert violations[0].rule == "variables_have_descriptions"

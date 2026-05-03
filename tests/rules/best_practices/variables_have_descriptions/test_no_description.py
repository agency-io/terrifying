"""Test that a variable with no description (None) is flagged."""

from pathlib import Path

from terrifying.core.context import TerraformContext, TerraformFile, Variable
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

"""Test that only variables missing descriptions are flagged in a mixed set."""

from pathlib import Path

from terrifying.core.context import TerraformContext, TerraformFile, Variable
from terrifying.rules.best_practices import VariablesHaveDescriptions

_FILE = Path("variables.tf")


def _make_context(*variables: Variable) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, variables=list(variables))
    return TerraformContext(files=[tf_file])


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

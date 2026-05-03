"""Test that a variable with a non-empty description is not flagged."""

from pathlib import Path

from terrifying.core.context import TerraformContext, TerraformFile, Variable
from terrifying.rules.best_practices import VariablesHaveDescriptions

_FILE = Path("variables.tf")


def _make_context(*variables: Variable) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, variables=list(variables))
    return TerraformContext(files=[tf_file])


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

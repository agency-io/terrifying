"""Test that no violations occur when there are no resources."""

from pathlib import Path

from terrifying.core.context import TerraformContext, TerraformFile
from terrifying.rules.best_practices import RequiredTags

_FILE = Path("main.tf")


def test_no_resources_no_violations():
    context = TerraformContext(files=[TerraformFile(path=_FILE)])
    violations = RequiredTags(tags=["Environment"]).check(context)
    assert violations == []

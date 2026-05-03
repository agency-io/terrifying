"""Test MaxResourcesPerFile: empty context produces no violations."""

from terrifying.core import TerraformContext
from terrifying.rules.structural import MaxResourcesPerFile


def test_empty_context_no_violations():
    rule = MaxResourcesPerFile()
    ctx = TerraformContext(files=[])
    assert rule.check(ctx) == []

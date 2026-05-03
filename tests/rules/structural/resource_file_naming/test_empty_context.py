"""Test ResourceFileNaming: empty context produces no violations."""

from terrifying.core import TerraformContext
from terrifying.rules.structural import ResourceFileNaming


def test_empty_context_no_violations():
    rule = ResourceFileNaming(pattern=r".*\.tf")
    ctx = TerraformContext(files=[])
    assert rule.check(ctx) == []

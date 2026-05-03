"""Test MaxLinesPerFile: empty context produces no violations."""

from terrifying.core import TerraformContext
from terrifying.rules.structural import MaxLinesPerFile


def test_empty_context_no_violations():
    rule = MaxLinesPerFile()
    ctx = TerraformContext(files=[])
    assert rule.check(ctx) == []

"""Test that an output with an empty string description is flagged."""

from pathlib import Path

from terrifying.core.context import Output, TerraformContext, TerraformFile
from terrifying.rules.best_practices import OutputsHaveDescriptions

_FILE = Path("outputs.tf")


def _make_context(*outputs: Output) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, outputs=list(outputs))
    return TerraformContext(files=[tf_file])


def test_empty_string_description_flagged():
    output = Output(name="vpc_id", description="", value="var.vpc_id", file=_FILE)
    violations = OutputsHaveDescriptions().check(_make_context(output))
    assert len(violations) == 1
    assert "vpc_id" in violations[0].message

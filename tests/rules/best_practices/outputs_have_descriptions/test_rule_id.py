"""Test that OutputsHaveDescriptions reports the correct rule identifier."""

from pathlib import Path

from terrifying.core.context import Output, TerraformContext, TerraformFile
from terrifying.rules.best_practices import OutputsHaveDescriptions

_FILE = Path("outputs.tf")


def _make_context(*outputs: Output) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, outputs=list(outputs))
    return TerraformContext(files=[tf_file])


def test_rule_id():
    output = Output(
        name="bucket_name", description=None, value="var.bucket", file=_FILE
    )
    violations = OutputsHaveDescriptions().check(_make_context(output))
    assert violations[0].rule == "outputs_have_descriptions"

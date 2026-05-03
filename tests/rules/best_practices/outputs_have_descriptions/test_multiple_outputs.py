"""Test that only outputs missing descriptions are flagged in a mixed set."""

from pathlib import Path

from terrifying.core.context import Output, TerraformContext, TerraformFile
from terrifying.rules.best_practices import OutputsHaveDescriptions

_FILE = Path("outputs.tf")


def _make_context(*outputs: Output) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, outputs=list(outputs))
    return TerraformContext(files=[tf_file])


def test_multiple_outputs_mixed():
    out_ok = Output(
        name="region",
        description="The deployed region",
        value="var.region",
        file=_FILE,
    )
    out_none = Output(name="env", description=None, value="var.env", file=_FILE)
    out_empty = Output(
        name="instance_id", description="", value="var.instance_id", file=_FILE
    )
    violations = OutputsHaveDescriptions().check(
        _make_context(out_ok, out_none, out_empty)
    )
    assert len(violations) == 2
    messages = {v.message for v in violations}
    assert any("env" in m for m in messages)
    assert any("instance_id" in m for m in messages)

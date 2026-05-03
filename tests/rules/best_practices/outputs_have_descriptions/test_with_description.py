"""Test that an output with a non-empty description is not flagged."""

from pathlib import Path

from terrifying.core.context import Output, TerraformContext, TerraformFile
from terrifying.rules.best_practices import OutputsHaveDescriptions

_FILE = Path("outputs.tf")


def _make_context(*outputs: Output) -> TerraformContext:
    tf_file = TerraformFile(path=_FILE, outputs=list(outputs))
    return TerraformContext(files=[tf_file])


def test_non_empty_description_not_flagged():
    output = Output(
        name="bucket_name",
        description="The S3 bucket name",
        value="var.bucket",
        file=_FILE,
    )
    violations = OutputsHaveDescriptions().check(_make_context(output))
    assert violations == []

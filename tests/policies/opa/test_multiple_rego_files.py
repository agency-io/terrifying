"""Test that multiple .rego files are each invoked via subprocess."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.policies.opa import OpaAdapter


def _make_context() -> TerraformContext:
    resource = Resource(
        type="aws_s3_bucket",
        name="bucket",
        attributes={"bucket": "my-bucket"},
        file=Path("main.tf"),
    )
    tf_file = TerraformFile(path=Path("main.tf"), resources=[resource], line_count=10)
    return TerraformContext(files=[tf_file])


def _opa_output(denials: list) -> str:
    return json.dumps({"result": [{"expressions": [{"value": denials}]}]})


def test_multiple_rego_files_all_invoked(tmp_path):
    (tmp_path / "alpha.rego").write_text("package terrifying")
    (tmp_path / "beta.rego").write_text("package terrifying")
    outputs = [
        MagicMock(stdout=_opa_output(["alpha violation"]), returncode=0),
        MagicMock(stdout=_opa_output(["beta violation"]), returncode=0),
    ]
    with patch(
        "terrifying.policies.opa.subprocess.run", side_effect=outputs
    ) as mock_run:
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert mock_run.call_count == 2
    assert len(violations) == 2
    rules = {v.rule for v in violations}
    assert rules == {"opa:alpha", "opa:beta"}

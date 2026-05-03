"""Tests for terrifying.policies.opa — OpaAdapter."""

import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from terrifying.core.context import Resource, TerraformContext, TerraformFile
from terrifying.policies.opa import OpaAdapter

# ── Helpers ───────────────────────────────────────────────────────────────────


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


# ── Empty policy dir ──────────────────────────────────────────────────────────


def test_empty_policy_dir_returns_no_violations(tmp_path):
    adapter = OpaAdapter(tmp_path)
    with patch("terrifying.policies.opa.subprocess.run") as mock_run:
        violations = adapter.run(_make_context())
    assert violations == []
    mock_run.assert_not_called()


# ── String denial ─────────────────────────────────────────────────────────────


def test_string_denial_creates_violation(tmp_path):
    policy = tmp_path / "mypolicy.rego"
    policy.write_text('package terrifying\ndeny = ["no buckets allowed"]')
    mock_result = MagicMock(stdout=_opa_output(["no buckets allowed"]), returncode=0)
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert len(violations) == 1
    assert violations[0].rule == "opa:mypolicy"
    assert violations[0].message == "no buckets allowed"
    assert violations[0].file == Path(".")


# ── Structured denial with file and line ─────────────────────────────────────


def test_structured_denial_populates_file_and_line(tmp_path):
    policy = tmp_path / "tags.rego"
    policy.write_text("package terrifying")
    denial = {"msg": "must have tags", "file": "main.tf", "line": 5}
    mock_result = MagicMock(stdout=_opa_output([denial]), returncode=0)
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == "opa:tags"
    assert v.message == "must have tags"
    assert v.file == Path("main.tf")
    assert v.line == 5


# ── Structured denial without file ───────────────────────────────────────────


def test_structured_denial_without_file_uses_dot(tmp_path):
    policy = tmp_path / "noloc.rego"
    policy.write_text("package terrifying")
    denial = {"msg": "something wrong"}
    mock_result = MagicMock(stdout=_opa_output([denial]), returncode=0)
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert len(violations) == 1
    assert violations[0].file == Path(".")
    assert violations[0].line is None


# ── Empty deny set ────────────────────────────────────────────────────────────


def test_empty_deny_set_produces_no_violations(tmp_path):
    policy = tmp_path / "ok.rego"
    policy.write_text("package terrifying")
    mock_result = MagicMock(stdout=_opa_output([]), returncode=0)
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert violations == []


# ── Multiple denials in one policy ───────────────────────────────────────────


def test_multiple_denials_produce_one_violation_each(tmp_path):
    policy = tmp_path / "multi.rego"
    policy.write_text("package terrifying")
    mock_result = MagicMock(
        stdout=_opa_output(["error one", "error two", "error three"]), returncode=0
    )
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert len(violations) == 3
    messages = {v.message for v in violations}
    assert messages == {"error one", "error two", "error three"}


# ── Multiple .rego files ──────────────────────────────────────────────────────


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


# ── FileNotFoundError → opa_unavailable ──────────────────────────────────────


def test_file_not_found_produces_opa_unavailable_violation(tmp_path):
    policy = tmp_path / "missing.rego"
    policy.write_text("package terrifying")
    with patch("terrifying.policies.opa.subprocess.run", side_effect=FileNotFoundError):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == "opa_unavailable"
    assert v.message == "opa binary not found on PATH"
    assert v.file == policy


# ── Rule format ───────────────────────────────────────────────────────────────


def test_rule_format_is_opa_colon_stem(tmp_path):
    policy = tmp_path / "enforce_naming.rego"
    policy.write_text("package terrifying")
    mock_result = MagicMock(stdout=_opa_output(["bad name"]), returncode=0)
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert violations[0].rule == "opa:enforce_naming"


# ── Malformed OPA output ──────────────────────────────────────────────────────


def test_malformed_json_produces_no_violations(tmp_path):
    policy = tmp_path / "bad.rego"
    policy.write_text("package terrifying")
    mock_result = MagicMock(stdout="not valid json", returncode=0)
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert violations == []


def test_unexpected_json_shape_produces_no_violations(tmp_path):
    policy = tmp_path / "weird.rego"
    policy.write_text("package terrifying")
    mock_result = MagicMock(stdout=json.dumps({"unexpected": "shape"}), returncode=0)
    with patch("terrifying.policies.opa.subprocess.run", return_value=mock_result):
        violations = OpaAdapter(tmp_path).run(_make_context())
    assert violations == []


# ── TerraformContext.to_json() sanity checks ─────────────────────────────────


def test_to_json_resource_fields_present():
    ctx = _make_context()
    result = ctx.to_json()
    assert "resources" in result
    resource = result["resources"][0]
    assert resource["type"] == "aws_s3_bucket"
    assert resource["name"] == "bucket"
    assert resource["attributes"] == {"bucket": "my-bucket"}
    assert resource["file"] == "main.tf"
    assert resource["line"] is None


def test_to_json_file_fields_present():
    ctx = _make_context()
    result = ctx.to_json()
    assert "files" in result
    file_dict = result["files"][0]
    assert file_dict["path"] == "main.tf"
    assert file_dict["line_count"] == 10
    assert "resources" in file_dict
    assert "variables" in file_dict
    assert "outputs" in file_dict


# ── Integration test (skipped if opa not installed) ───────────────────────────


@pytest.mark.skipif(shutil.which("opa") is None, reason="opa not installed")
def test_integration_with_real_opa(tmp_path):
    policy = tmp_path / "test_policy.rego"
    policy.write_text(
        'package terrifying\n\ndeny contains msg if {\n  msg := "always deny"\n}\n'
    )
    ctx = _make_context()
    violations = OpaAdapter(tmp_path).run(ctx)
    assert len(violations) >= 1
    assert violations[0].rule == "opa:test_policy"

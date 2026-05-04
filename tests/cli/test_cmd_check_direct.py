"""Unit tests for _cmd_check covering JSON format and violation_to_dict."""

import argparse
import json
import pytest
from terrifying.cli import _cmd_check


def test_cmd_check_json_format_no_violations(tmp_path, capsys):
    (tmp_path / "main.tf").write_text('resource "aws_s3_bucket" "b" {}\n')
    args = argparse.Namespace(directory=str(tmp_path), format="json")
    with pytest.raises(SystemExit) as exc:
        _cmd_check(args)
    assert exc.value.code == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert isinstance(data, list)


def test_cmd_check_json_format_with_violation(tmp_path, capsys):
    cfg = tmp_path / "terrifying.yml"
    cfg.write_text(
        "terraform:\n  path: .\nrules:\n  required_tags:\n    tags:\n      - Env\n"
    )
    tf = tmp_path / "main.tf"
    tf.write_text('resource "aws_s3_bucket" "b" {}\n')
    args = argparse.Namespace(directory=str(tmp_path), format="json")
    with pytest.raises(SystemExit):
        _cmd_check(args)
    out = capsys.readouterr().out
    data = json.loads(out)
    assert isinstance(data, list)
    if data:
        assert "rule" in data[0]
        assert "message" in data[0]


def test_violation_to_dict_direct():
    from terrifying.cli import _violation_to_dict
    from terrifying.core.rule import Violation

    v = Violation(
        rule="test_rule", file="main.tf", message="oops", severity="error", line=5
    )
    d = _violation_to_dict(v)
    assert d["rule"] == "test_rule"
    assert d["file"] == "main.tf"
    assert d["line"] == 5
    assert d["severity"] == "error"
    assert d["message"] == "oops"

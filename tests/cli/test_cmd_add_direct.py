"""Unit tests for _cmd_add — covers add command code paths."""

import argparse
from unittest.mock import patch
from terrifying.cli import _cmd_add


def test_cmd_add_dry_run(tmp_path, capsys):
    args = argparse.Namespace(
        policy_ids=["rds-storage-encrypted"],
        engine="rego",
        dry_run=True,
    )
    with patch("terrifying.policies.add.Path.cwd", return_value=tmp_path):
        _cmd_add(args)
    out = capsys.readouterr().out
    assert "dry-run" in out


def test_cmd_add_both_engines_dry_run(tmp_path, capsys):
    args = argparse.Namespace(
        policy_ids=["rds-storage-encrypted"],
        engine="both",
        dry_run=True,
    )
    with patch("terrifying.policies.add.Path.cwd", return_value=tmp_path):
        _cmd_add(args)
    out = capsys.readouterr().out
    assert "dry-run" in out


def test_cmd_add_unknown_policy_id_exits(tmp_path, capsys):
    import pytest

    args = argparse.Namespace(
        policy_ids=["nonexistent-policy-xyz-abc"],
        engine="rego",
        dry_run=False,
    )
    with pytest.raises(SystemExit) as exc:
        _cmd_add(args)
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "nonexistent-policy-xyz-abc" in err

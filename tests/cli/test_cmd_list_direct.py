"""Unit tests for _cmd_list — covers the list command code paths."""

import argparse
from terrifying.cli import _cmd_list


def test_cmd_list_all(capsys):
    args = argparse.Namespace(engine="both", tags=None)
    _cmd_list(args)
    out = capsys.readouterr().out
    assert "policies" in out


def test_cmd_list_engine_rego(capsys):
    args = argparse.Namespace(engine="rego", tags=None)
    _cmd_list(args)
    out = capsys.readouterr().out
    assert "[rego]" in out


def test_cmd_list_with_tag(capsys):
    args = argparse.Namespace(engine="both", tags=["fsbp"])
    _cmd_list(args)
    out = capsys.readouterr().out
    assert "policies" in out


def test_cmd_list_no_match(capsys):
    args = argparse.Namespace(engine="both", tags=["nonexistent-tag-xyz-abc"])
    _cmd_list(args)
    out = capsys.readouterr().out
    assert "No policies match" in out

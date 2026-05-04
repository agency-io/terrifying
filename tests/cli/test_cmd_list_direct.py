"""Unit tests for _cmd_list — covers the list command code paths."""

import argparse
import json
from terrifying.cli import _cmd_list


def _ns(**kwargs):
    return argparse.Namespace(format="text", **kwargs)


def test_cmd_list_all(capsys):
    _cmd_list(_ns(engine="both", tags=None))
    out = capsys.readouterr().out
    assert "policies" in out


def test_cmd_list_engine_rego(capsys):
    _cmd_list(_ns(engine="rego", tags=None))
    out = capsys.readouterr().out
    assert "[rego]" in out


def test_cmd_list_with_tag(capsys):
    _cmd_list(_ns(engine="both", tags=["fsbp"]))
    out = capsys.readouterr().out
    assert "policies" in out


def test_cmd_list_no_match(capsys):
    _cmd_list(_ns(engine="both", tags=["nonexistent-tag-xyz-abc"]))
    out = capsys.readouterr().out
    assert "No policies match" in out


def test_cmd_list_json_format(capsys):
    _cmd_list(argparse.Namespace(engine="both", tags=None, format="json"))
    out = capsys.readouterr().out
    data = json.loads(out)
    assert isinstance(data, list)
    assert len(data) > 0
    entry = data[0]
    assert {
        "id",
        "engine",
        "service",
        "severity",
        "description",
        "terraform_resources",
        "tags",
    } <= entry.keys()


def test_cmd_list_json_full_description(capsys):
    _cmd_list(argparse.Namespace(engine="rego", tags=None, format="json"))
    out = capsys.readouterr().out
    data = json.loads(out)
    assert all(
        isinstance(e["description"], str) and len(e["description"]) > 0 for e in data
    )


def test_cmd_list_json_filtered(capsys):
    _cmd_list(argparse.Namespace(engine="rego", tags=["s3"], format="json"))
    out = capsys.readouterr().out
    data = json.loads(out)
    assert all(e["engine"] == "rego" for e in data)
    assert all("s3" in e["tags"] for e in data)

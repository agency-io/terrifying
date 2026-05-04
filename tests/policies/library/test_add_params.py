"""Tests for _collect_params and _build_delta covering param-related paths."""

import dataclasses
from unittest.mock import patch
from terrifying.policies.library import PolicyEntry, ParamDescriptor
from terrifying.policies.add import _collect_params, _build_delta, run_add


def _make_entry(id_, engine, params=None):
    return PolicyEntry(
        id=id_,
        engine=engine,
        service="test",
        file=f"test/{id_}.{'rego' if engine == 'rego' else 'yml'}",
        description="test policy",
        severity="High",
        terraform_resources=["aws_test"],
        tags=["test"],
        params=params or [],
    )


def test_collect_params_prompts_for_new_params(tmp_path):
    entry = _make_entry(
        "p1",
        "rego",
        [
            ParamDescriptor(
                name="min_days", type="str", description="min days", default=7
            )
        ],
    )
    with patch("builtins.input", return_value="30") as mock_input:
        result = _collect_params([entry], {})
    assert "min_days" in result["opa"]
    assert result["opa"]["min_days"] == "30"
    mock_input.assert_called_once()


def test_collect_params_uses_default_on_empty_input():
    entry = _make_entry(
        "p1",
        "rego",
        [
            ParamDescriptor(
                name="min_days", type="str", description="min days", default=7
            )
        ],
    )
    with patch("builtins.input", return_value=""):
        result = _collect_params([entry], {})
    assert result["opa"]["min_days"] == 7


def test_collect_params_shared_params_both_engines(capsys):
    rego = _make_entry(
        "p1",
        "rego",
        [
            ParamDescriptor(
                name="tags", type="str", description="required tags", default=None
            )
        ],
    )
    c7n = _make_entry(
        "p2",
        "c7n",
        [
            ParamDescriptor(
                name="tags", type="str", description="required tags", default=None
            )
        ],
    )
    with patch("builtins.input", return_value="Env"):
        result = _collect_params([rego, c7n], {})
    out = capsys.readouterr().out
    assert "shared" in out
    assert "tags" in result["opa"]
    assert "tags" in result["c7n"]


def test_collect_params_skips_existing():
    entry = _make_entry(
        "p1",
        "rego",
        [ParamDescriptor(name="min_days", type="str", description="x", default=7)],
    )
    existing_config = {"policies": {"opa": {"params": {"min_days": 14}}}}
    with patch("builtins.input", side_effect=AssertionError("should not prompt")) as m:
        result = _collect_params([entry], existing_config)
    assert result["opa"] == {}


def test_collect_params_eofError_uses_default():
    entry = _make_entry(
        "p1",
        "rego",
        [ParamDescriptor(name="x", type="str", description="x", default="fallback")],
    )
    with patch("builtins.input", side_effect=EOFError):
        result = _collect_params([entry], {})
    assert result["opa"]["x"] == "fallback"


def test_build_delta_with_c7n_entry(tmp_path):
    entry = _make_entry("rds-storage-encrypted", "c7n")
    # Point file to actual library file
    from terrifying.policies.library import load_manifest, filter_by_engine

    entries = [
        e
        for e in filter_by_engine(load_manifest(), "c7n")
        if e.id == "rds-storage-encrypted"
    ]
    if not entries:
        return
    delta = _build_delta(entries, {"opa": {}, "c7n": {}}, tmp_path / "terrifying.yml")
    assert any(op.engine == "c7n" for op in delta.file_ops)


def test_run_add_aborts_when_not_confirmed(tmp_path, capsys):
    entries = []
    from terrifying.policies.library import load_manifest, filter_by_engine

    entries = [
        e
        for e in filter_by_engine(load_manifest(), "rego")
        if e.id == "rds-storage-encrypted"
    ]
    with (
        patch("builtins.input", return_value="n"),
        patch("terrifying.policies.add.Path.cwd", return_value=tmp_path),
    ):
        run_add(entries, dry_run=False)
    out = capsys.readouterr().out
    assert "Aborted" in out
    assert list(tmp_path.rglob("*.rego")) == []


def test_run_add_existing_param_notification(tmp_path, capsys):
    cfg = tmp_path / "terrifying.yml"
    cfg.write_text("policies:\n  opa:\n    params:\n      min_days: 14\n")
    entry = _make_entry(
        "p1",
        "rego",
        [ParamDescriptor(name="min_days", type="str", description="x", default=7)],
    )
    from terrifying.policies.library import get_policy_source

    with (
        patch("terrifying.policies.add.Path.cwd", return_value=tmp_path),
        patch("terrifying.policies.library.get_policy_source", return_value="# stub"),
        patch("builtins.input", return_value="n"),
    ):
        run_add([entry], dry_run=False)
    out = capsys.readouterr().out
    assert "already set" in out


def test_build_delta_with_opa_params(tmp_path):
    """Covers lines 159-160: new_params.get("opa") branch."""
    from terrifying.policies.library import load_manifest, filter_by_engine

    entries = [
        e
        for e in filter_by_engine(load_manifest(), "rego")
        if e.id == "rds-storage-encrypted"
    ]
    param = ParamDescriptor(
        name="test_param", type="str", description="x", default="val"
    )
    # Patch the entry to have a param
    patched = dataclasses.replace(entries[0], params=[param])
    with patch("builtins.input", return_value="myval"):
        result = _collect_params([patched], {})
    assert result["opa"].get("test_param") == "myval"
    delta = _build_delta([patched], result, tmp_path / "terrifying.yml")
    assert (
        delta.new_config["policies"]["opa"].get("params", {}).get("test_param")
        == "myval"
    )


def test_build_delta_c7n_with_params(tmp_path):
    """Covers lines 163-169: c7n section creation and params."""
    from terrifying.policies.library import load_manifest, filter_by_engine

    entries = [
        e
        for e in filter_by_engine(load_manifest(), "c7n")
        if e.id == "rds-storage-encrypted"
    ]
    if not entries:
        return
    param = ParamDescriptor(
        name="c7n_param", type="str", description="x", default="default_val"
    )
    patched = dataclasses.replace(entries[0], params=[param])
    with patch("builtins.input", return_value="newval"):
        result = _collect_params([patched], {})
    delta = _build_delta([patched], result, tmp_path / "terrifying.yml")
    assert "c7n" in delta.new_config["policies"]
    assert (
        delta.new_config["policies"]["c7n"].get("params", {}).get("c7n_param")
        == "newval"
    )

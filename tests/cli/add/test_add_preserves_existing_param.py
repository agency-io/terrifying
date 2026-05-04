from unittest.mock import patch
from terrifying.policies.library import (
    load_manifest,
    filter_by_engine,
    ParamDescriptor,
)
from terrifying.policies.add import run_add
import yaml


def _entry_with_param():
    base = [
        e
        for e in filter_by_engine(load_manifest(), "rego")
        if e.id == "rds-storage-encrypted"
    ][0]
    import dataclasses

    return dataclasses.replace(
        base,
        params=[
            ParamDescriptor(
                "required_tags", "list[string]", "Required tag keys", ["Environment"]
            )
        ],
    )


def test_preserves_existing_param(tmp_path):
    config_text = "policies:\n  opa:\n    path: ./policies/opa\n    params:\n      required_tags: [ExistingValue]\n"
    (tmp_path / "terrifying.yml").write_text(config_text)
    entry = _entry_with_param()
    with (
        patch("builtins.input", return_value="y"),
        patch("terrifying.policies.add.Path.cwd", return_value=tmp_path),
    ):
        run_add([entry], dry_run=False)
    config = yaml.safe_load((tmp_path / "terrifying.yml").read_text())
    assert config["policies"]["opa"]["params"]["required_tags"] == ["ExistingValue"]

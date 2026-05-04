from pathlib import Path
from unittest.mock import patch
from terrifying.policies.library import load_manifest, filter_by_engine
from terrifying.policies.add import run_add


def test_add_noninteractive_rego(tmp_path):
    entries = [e for e in filter_by_engine(load_manifest(), "rego") if e.id == "rds-storage-encrypted"]
    assert entries, "rds-storage-encrypted rego entry not in manifest"
    with patch("builtins.input", return_value="y"), patch("terrifying.policies.add.Path.cwd", return_value=tmp_path):
        run_add(entries, dry_run=False)
    written = list(tmp_path.glob("policies/opa/*.rego"))
    assert any("rds-storage-encrypted" in f.name for f in written)

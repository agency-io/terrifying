from unittest.mock import patch
from terrifying.policies.library import load_manifest, filter_by_engine
from terrifying.policies.add import run_add


def test_dry_run_writes_no_files(tmp_path):
    entries = [e for e in filter_by_engine(load_manifest(), "rego") if e.id == "rds-storage-encrypted"]
    with patch("terrifying.policies.add.Path.cwd", return_value=tmp_path):
        run_add(entries, dry_run=True)
    assert list(tmp_path.rglob("*.rego")) == []

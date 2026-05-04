from unittest.mock import patch
from terrifying.policies.library import load_manifest, filter_by_engine
from terrifying.policies.add import run_add


def test_add_both_engines(tmp_path):
    all_entries = filter_by_engine(load_manifest(), "both")
    entries = [e for e in all_entries if e.id == "rds-storage-encrypted"]
    assert len(entries) == 2, "Expected both rego and c7n variants"
    with patch("builtins.input", return_value="y"), patch("terrifying.policies.add.Path.cwd", return_value=tmp_path):
        run_add(entries, dry_run=False)
    assert any(tmp_path.glob("policies/opa/*.rego"))
    assert any(tmp_path.glob("policies/c7n/*.yml"))

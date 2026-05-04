from unittest.mock import patch
from terrifying.policies.library import load_manifest, filter_by_engine
from terrifying.policies.add import run_add


def test_skips_existing_file(tmp_path, capsys):
    entries = [e for e in filter_by_engine(load_manifest(), "rego") if e.id == "rds-storage-encrypted"]
    opa_dir = tmp_path / "policies/opa"
    opa_dir.mkdir(parents=True)
    existing = opa_dir / "rds-storage-encrypted.rego"
    existing.write_text("# existing content")
    original_content = existing.read_text()
    with patch("builtins.input", return_value="y"), patch("terrifying.policies.add.Path.cwd", return_value=tmp_path):
        run_add(entries, dry_run=False)
    assert existing.read_text() == original_content
    out = capsys.readouterr().out
    assert "WARNING" in out or "skipping" in out.lower()

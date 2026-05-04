from unittest.mock import patch
from terrifying.policies.library import load_manifest, filter_by_engine
from terrifying.policies.add import run_add
import yaml


def test_creates_opa_section_when_missing(tmp_path):
    entries = [e for e in filter_by_engine(load_manifest(), "rego") if e.id == "rds-storage-encrypted"]
    # No terrifying.yml exists
    with patch("builtins.input", return_value="y"), patch("terrifying.policies.add.Path.cwd", return_value=tmp_path):
        run_add(entries, dry_run=False)
    config = yaml.safe_load((tmp_path / "terrifying.yml").read_text())
    assert "policies" in config
    assert "opa" in config["policies"]
    assert "path" in config["policies"]["opa"]

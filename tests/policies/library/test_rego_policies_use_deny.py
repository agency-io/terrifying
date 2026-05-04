import importlib.resources
from terrifying.policies.library import load_manifest


def test_rego_policies_use_deny():
    pkg = importlib.resources.files("terrifying.policies.library")
    entries = [e for e in load_manifest() if e.engine == "rego"]
    assert len(entries) > 0
    for entry in entries:
        source = (pkg / entry.file).read_text(encoding="utf-8")
        assert "deny contains" in source, (
            f"{entry.file}: expected 'deny contains' but found 'violation' pattern — "
            "policy was not rewritten to use the terrifying deny convention"
        )
        assert (
            "violation contains" not in source
        ), f"{entry.file}: still uses old 'violation contains' pattern"

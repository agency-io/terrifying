import pytest
from terrifying.policies.library import load_manifest, get_policy_source


def test_get_policy_source_returns_content():
    entries = load_manifest()
    entry = entries[0]
    source = get_policy_source(entry)
    assert len(source) > 0


def test_get_policy_source_rego_has_package():
    entries = load_manifest()
    rego_entries = [e for e in entries if e.engine == "rego"]
    entry = rego_entries[0]
    source = get_policy_source(entry)
    assert "package terrifying" in source


def test_get_policy_source_c7n_has_policies_key():
    entries = load_manifest()
    c7n_entries = [e for e in entries if e.engine == "c7n"]
    entry = c7n_entries[0]
    source = get_policy_source(entry)
    assert "policies:" in source

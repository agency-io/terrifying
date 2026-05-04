from terrifying.policies.library import load_manifest, filter_by_engine


def test_filter_rego():
    entries = load_manifest()
    result = filter_by_engine(entries, "rego")
    assert all(e.engine == "rego" for e in result)
    assert len(result) > 0


def test_filter_c7n():
    entries = load_manifest()
    result = filter_by_engine(entries, "c7n")
    assert all(e.engine == "c7n" for e in result)
    assert len(result) > 0


def test_filter_both_returns_all():
    entries = load_manifest()
    result = filter_by_engine(entries, "both")
    assert len(result) == len(entries)

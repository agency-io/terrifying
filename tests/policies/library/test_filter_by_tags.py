from terrifying.policies.library import load_manifest, filter_by_tags


def test_filter_by_single_tag():
    entries = load_manifest()
    result = filter_by_tags(entries, ["rego"])
    assert all(e.has_tag("rego") for e in result)
    assert len(result) > 0


def test_filter_by_multiple_tags_all_must_match():
    entries = load_manifest()
    result = filter_by_tags(entries, ["rego", "s3"])
    assert all(e.has_tag("rego") and e.has_tag("s3") for e in result)


def test_filter_by_nonexistent_tag_returns_empty():
    entries = load_manifest()
    result = filter_by_tags(entries, ["nonexistent-tag-xyz"])
    assert result == []

from terrifying.policies.library import load_manifest


def test_manifest_loads():
    entries = load_manifest()
    assert len(entries) > 0

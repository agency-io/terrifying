import importlib.resources
from terrifying.policies.library import load_manifest


def test_c7n_policies_no_mode_block():
    pkg = importlib.resources.files("terrifying.policies.library")
    entries = [e for e in load_manifest() if e.engine == "c7n"]
    assert len(entries) > 0
    for entry in entries:
        source = (pkg / entry.file).read_text(encoding="utf-8")
        import re
        assert not re.search(r"^\s+mode:\s*$", source, re.MULTILINE), (
            f"{entry.file}: contains c7n 'mode:' block — runtime c7n mode not stripped"
        )

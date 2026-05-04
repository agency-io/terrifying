import importlib.resources
from terrifying.policies.library import load_manifest


def test_manifest_entries_valid():
    entries = load_manifest()
    pkg = importlib.resources.files("terrifying.policies.library")
    for entry in entries:
        assert entry.id, f"Entry missing id: {entry}"
        assert entry.engine in ("rego", "c7n"), f"Bad engine: {entry.engine}"
        assert entry.service, f"Entry missing service: {entry.id}"
        assert entry.file, f"Entry missing file: {entry.id}"
        assert entry.description, f"Entry missing description: {entry.id}"
        assert (pkg / entry.file).is_file(), f"Policy file missing: {entry.file}"

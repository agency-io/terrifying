"""Test that temp files are removed after c7n-left returns."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.policies.c7n import C7nAdapter

_CREATED_TEMP_FILES: list[Path] = []


def test_temp_file_cleaned_up(tmp_path: Path) -> None:
    """Temp file created for rendered policy is deleted after c7n-left runs."""
    policy = tmp_path / "check.yml"
    policy.write_text(
        "policies:\n  - name: check\n    resource: terraform.aws_s3_bucket\n"
    )
    adapter = C7nAdapter(tmp_path)

    created_paths: list[Path] = []
    original_named_temp = tempfile.NamedTemporaryFile

    class _TrackingTempFile:
        """Context manager that wraps NamedTemporaryFile and records the path."""

        def __init__(self, **kwargs):
            self._f = original_named_temp(**kwargs)
            self.name = self._f.name
            created_paths.append(Path(self.name))

        def __enter__(self):
            self._f.__enter__()
            return self

        def __exit__(self, *args):
            return self._f.__exit__(*args)

        def write(self, data):
            self._f.write(data)

    mock_result = MagicMock(stdout=json.dumps([]), returncode=0)
    with patch("terrifying.policies.c7n.subprocess.run", return_value=mock_result):
        with patch(
            "terrifying.policies.c7n.tempfile.NamedTemporaryFile", _TrackingTempFile
        ):
            adapter.run(Path("/some/tf"))

    assert len(created_paths) == 1
    assert not created_paths[0].exists(), "Temp file should have been deleted"

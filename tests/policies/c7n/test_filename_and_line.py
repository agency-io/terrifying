"""Tests for the C7nAdapter policy adapter."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.policies.c7n import C7nAdapter

_ONE_MATCH = [
    {
        "policy": {"name": "require-tags"},
        "resources": [
            {
                "__tfmeta": {"filename": "main.tf", "line_start": 5},
                "type": "aws_s3_bucket",
                "name": "bucket",
            }
        ],
    }
]


def _make_adapter(tmp_path: Path, *, with_policy: bool = True) -> C7nAdapter:
    if with_policy:
        (tmp_path / "policy.yml").write_text("policies: []\n")
    return C7nAdapter(policy_dir=tmp_path)


def _mock_run(stdout_data: object) -> MagicMock:
    return MagicMock(stdout=json.dumps(stdout_data), returncode=0)


def test_tfmeta_filename_and_line_start_populated(tmp_path: Path) -> None:
    """file and line on the Violation should reflect __tfmeta values."""
    adapter = _make_adapter(tmp_path)
    with patch(
        "terrifying.policies.c7n.subprocess.run", return_value=_mock_run(_ONE_MATCH)
    ):
        violations = adapter.run(Path("/tf"))

    v = violations[0]
    assert v.file == Path("main.tf")
    assert v.line == 5

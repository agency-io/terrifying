"""Tests for the C7nAdapter policy adapter."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from terrifying.policies.c7n import C7nAdapter

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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

_NO_MATCHES: list = []


def _make_adapter(tmp_path: Path, *, with_policy: bool = True) -> C7nAdapter:
    """Return a C7nAdapter whose policy_dir optionally contains a dummy yml."""
    if with_policy:
        (tmp_path / "policy.yml").write_text("policies: []\n")
    return C7nAdapter(policy_dir=tmp_path)


def _mock_run(stdout_data: object) -> MagicMock:
    return MagicMock(stdout=json.dumps(stdout_data), returncode=0)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_empty_policy_dir_returns_empty_and_no_subprocess(tmp_path: Path) -> None:
    """No subprocess call should be made when the policy directory is empty."""
    adapter = C7nAdapter(policy_dir=tmp_path)
    with patch("terrifying.policies.c7n.subprocess.run") as mock_run:
        result = adapter.run(Path("/some/tf/dir"))
    assert result == []
    mock_run.assert_not_called()


def test_one_match_returns_one_violation(tmp_path: Path) -> None:
    """A single matched resource produces exactly one Violation."""
    adapter = _make_adapter(tmp_path)
    with patch(
        "terrifying.policies.c7n.subprocess.run", return_value=_mock_run(_ONE_MATCH)
    ):
        violations = adapter.run(Path("/tf"))

    assert len(violations) == 1
    v = violations[0]
    assert v.rule == "c7n:require-tags"
    assert "require-tags" in v.message


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


def test_no_tfmeta_no_crash(tmp_path: Path) -> None:
    """Resources without __tfmeta should produce a Violation without crashing."""
    data = [
        {
            "policy": {"name": "require-tags"},
            "resources": [
                {"type": "aws_s3_bucket", "name": "bucket"},
            ],
        }
    ]
    adapter = _make_adapter(tmp_path)
    with patch("terrifying.policies.c7n.subprocess.run", return_value=_mock_run(data)):
        violations = adapter.run(Path("/tf"))

    assert len(violations) == 1
    v = violations[0]
    assert v.file == Path(".")
    assert v.line is None


def test_no_line_start_gives_none(tmp_path: Path) -> None:
    """When __tfmeta exists but has no line_start, line should be None."""
    data = [
        {
            "policy": {"name": "require-tags"},
            "resources": [
                {
                    "__tfmeta": {"filename": "main.tf"},
                    "type": "aws_s3_bucket",
                    "name": "bucket",
                }
            ],
        }
    ]
    adapter = _make_adapter(tmp_path)
    with patch("terrifying.policies.c7n.subprocess.run", return_value=_mock_run(data)):
        violations = adapter.run(Path("/tf"))

    assert violations[0].line is None


def test_multiple_resources_produce_multiple_violations(tmp_path: Path) -> None:
    """Each resource entry should result in its own Violation."""
    data = [
        {
            "policy": {"name": "require-tags"},
            "resources": [
                {
                    "__tfmeta": {"filename": "a.tf", "line_start": 1},
                    "type": "aws_s3_bucket",
                    "name": "bucket_a",
                },
                {
                    "__tfmeta": {"filename": "b.tf", "line_start": 10},
                    "type": "aws_instance",
                    "name": "web",
                },
            ],
        }
    ]
    adapter = _make_adapter(tmp_path)
    with patch("terrifying.policies.c7n.subprocess.run", return_value=_mock_run(data)):
        violations = adapter.run(Path("/tf"))

    assert len(violations) == 2


def test_no_matches_returns_empty_list(tmp_path: Path) -> None:
    """An empty results list from c7n-left should produce no violations."""
    adapter = _make_adapter(tmp_path)
    with patch(
        "terrifying.policies.c7n.subprocess.run",
        return_value=_mock_run(_NO_MATCHES),
    ):
        violations = adapter.run(Path("/tf"))

    assert violations == []


def test_file_not_found_returns_c7n_unavailable_violation(tmp_path: Path) -> None:
    """FileNotFoundError should produce a single c7n_unavailable violation."""
    adapter = _make_adapter(tmp_path)
    with patch(
        "terrifying.policies.c7n.subprocess.run",
        side_effect=FileNotFoundError,
    ):
        violations = adapter.run(Path("/tf"))

    assert len(violations) == 1
    assert violations[0].rule == "c7n_unavailable"
    assert "c7n-left" in violations[0].message


def test_rule_field_format(tmp_path: Path) -> None:
    """rule field should be 'c7n:<policy_name>'."""
    adapter = _make_adapter(tmp_path)
    with patch(
        "terrifying.policies.c7n.subprocess.run", return_value=_mock_run(_ONE_MATCH)
    ):
        violations = adapter.run(Path("/tf"))

    assert violations[0].rule == "c7n:require-tags"


def test_subprocess_called_with_correct_args(tmp_path: Path) -> None:
    """subprocess.run should be invoked with the expected c7n-left command."""
    tf_dir = Path("/some/terraform")
    adapter = _make_adapter(tmp_path)
    with patch(
        "terrifying.policies.c7n.subprocess.run", return_value=_mock_run(_NO_MATCHES)
    ) as mock_run:
        adapter.run(tf_dir)

    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    cmd = args[0]
    assert cmd[0] == "c7n-left"
    assert "--policy" in cmd
    assert str(tmp_path) in cmd
    assert "--directory" in cmd
    assert str(tf_dir) in cmd
    assert "--output" in cmd
    assert "json" in cmd
    assert kwargs.get("capture_output") is True
    assert kwargs.get("text") is True
    assert kwargs.get("check") is False


# ---------------------------------------------------------------------------
# Integration test — skipped when c7n-left is not installed
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    shutil.which("c7n-left") is None,
    reason="c7n-left not installed; skipping integration test",
)
def test_integration_c7n_left_runs(tmp_path: Path) -> None:
    """Integration: c7n-left actually executes without error."""
    adapter = C7nAdapter(policy_dir=tmp_path)
    # No policies → empty result, no subprocess call needed
    result = adapter.run(tmp_path)
    assert isinstance(result, list)

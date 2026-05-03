"""Tests for the C7nAdapter policy adapter."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from terrifying.policies.c7n import C7nAdapter


def _make_adapter(tmp_path: Path, *, with_policy: bool = True) -> C7nAdapter:
    if with_policy:
        (tmp_path / "policy.yml").write_text("policies: []\n")
    return C7nAdapter(policy_dir=tmp_path)


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

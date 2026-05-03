"""Test that providing a non-existent directory exits with code 1."""

from unittest.mock import patch

import pytest

from terrifying.cli import main


def test_missing_directory(tmp_path):
    """A non-existent directory argument causes exit code 1."""
    missing = tmp_path / "does_not_exist"
    with patch("sys.argv", ["terrifying", "check", str(missing)]):
        with pytest.raises(SystemExit) as exc_info:
            main()
    assert exc_info.value.code == 1

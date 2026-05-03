"""Test that a directory producing an error violation exits with code 1."""

from pathlib import Path
from unittest.mock import patch

import pytest

from terrifying.cli import main
from terrifying.core.rule import Violation


def test_error_violation_exit_1(tmp_path):
    """An error-severity violation causes exit code 1."""
    tf = tmp_path / "main.tf"
    tf.write_text("")
    violation = Violation(
        rule="test", file=Path("main.tf"), message="bad", severity="error"
    )
    with patch("sys.argv", ["terrifying", "check", str(tmp_path)]):
        with patch("terrifying.cli.Path.cwd", return_value=tmp_path):
            with patch("terrifying.cli.Runner.run", return_value=[violation]):
                with pytest.raises(SystemExit) as exc_info:
                    main()
    assert exc_info.value.code == 1

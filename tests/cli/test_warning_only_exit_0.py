"""Test that warning-only violations exit with code 0."""

from pathlib import Path
from unittest.mock import patch

import pytest

from terrifying.cli import main
from terrifying.core.rule import Violation


def test_warning_only_exit_0(tmp_path):
    """Warning-severity violations do not trigger exit code 1."""
    tf = tmp_path / "main.tf"
    tf.write_text("")
    violation = Violation(
        rule="test", file=Path("main.tf"), message="ok", severity="warning"
    )
    with patch("sys.argv", ["terrifying", "check", str(tmp_path)]):
        with patch("terrifying.cli.Path.cwd", return_value=tmp_path):
            with patch("terrifying.cli.Runner.run", return_value=[violation]):
                with pytest.raises(SystemExit) as exc_info:
                    main()
    assert exc_info.value.code == 0

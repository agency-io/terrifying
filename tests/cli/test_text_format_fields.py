"""Test that text format output contains file, rule, severity, and message."""

from pathlib import Path
from unittest.mock import patch

import pytest

from terrifying.cli import main
from terrifying.core.rule import Violation


def test_text_format_fields(tmp_path, capsys):
    """Text format output contains the file, rule, severity, and message fields."""
    tf = tmp_path / "main.tf"
    tf.write_text("")
    violation = Violation(
        rule="my_rule",
        file=Path("main.tf"),
        message="something wrong",
        line=42,
        severity="error",
    )
    with patch("sys.argv", ["terrifying", "check", str(tmp_path)]):
        with patch("terrifying.cli.Path.cwd", return_value=tmp_path):
            with patch("terrifying.cli.Runner.run", return_value=[violation]):
                with pytest.raises(SystemExit):
                    main()
    out = capsys.readouterr().out
    assert "my_rule" in out
    assert "error" in out
    assert "something wrong" in out
    assert "main.tf" in out
    assert "42" in out

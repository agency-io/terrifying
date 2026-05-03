"""Test that a clean Terraform directory with no violations exits with code 0."""

from unittest.mock import patch

import pytest

from terrifying.cli import main


def test_no_violations_exit_0(tmp_path):
    """Running check on a directory with no violations exits 0."""
    tf = tmp_path / "main.tf"
    tf.write_text('variable "env" { description = "env" }\n')
    with patch("sys.argv", ["terrifying", "check", str(tmp_path)]):
        with patch("terrifying.cli.Path.cwd", return_value=tmp_path):
            with pytest.raises(SystemExit) as exc_info:
                main()
    assert exc_info.value.code == 0

"""Test that --format json outputs valid JSON."""

import json
from unittest.mock import patch

import pytest

from terrifying.cli import main


def test_format_json(tmp_path, capsys):
    """--format json produces valid JSON output."""
    tf = tmp_path / "main.tf"
    tf.write_text("")
    with patch("sys.argv", ["terrifying", "check", str(tmp_path), "--format", "json"]):
        with patch("terrifying.cli.Path.cwd", return_value=tmp_path):
            with pytest.raises(SystemExit):
                main()
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert isinstance(result, list)

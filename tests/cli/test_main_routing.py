"""Unit tests for main() routing — covers elif/else branches."""

import pytest
from unittest.mock import patch
from terrifying.cli import main


def test_main_no_command_exits():
    with patch("sys.argv", ["terrifying"]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 1


def test_main_list_command(capsys):
    with patch("sys.argv", ["terrifying", "list", "--engine", "rego"]):
        main()
    out = capsys.readouterr().out
    assert "policies" in out


def test_main_add_dry_run(tmp_path, capsys):
    with patch(
        "sys.argv",
        ["terrifying", "add", "rds-storage-encrypted", "--engine", "rego", "--dry-run"],
    ):
        with patch("terrifying.policies.add.Path.cwd", return_value=tmp_path):
            main()
    out = capsys.readouterr().out
    assert "dry-run" in out

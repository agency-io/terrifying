"""Tests for the `terrifying skill` CLI command."""

import argparse
import subprocess
import sys
from unittest.mock import patch

from terrifying.cli import _cmd_skill
from terrifying.skill import CLAUDE_CODE_SKILL, ISSUES_URL


def _ns(**kwargs):
    return argparse.Namespace(**kwargs)


def test_claude_code_format_outputs_skill(capsys):
    _cmd_skill(_ns(format="claude-code"))
    out = capsys.readouterr().out
    assert "terrifying" in out
    assert "deny" in out
    assert "package terrifying" in out


def test_claude_code_format_matches_constant(capsys):
    _cmd_skill(_ns(format="claude-code"))
    out = capsys.readouterr().out
    assert out == CLAUDE_CODE_SKILL


def test_unsupported_format_prints_message(capsys):
    _cmd_skill(_ns(format="cursor"))
    out = capsys.readouterr().out
    assert "not yet supported" in out
    assert ISSUES_URL in out


def test_unsupported_format_includes_format_name(capsys):
    _cmd_skill(_ns(format="windsurf"))
    out = capsys.readouterr().out
    assert "windsurf" in out


def test_cli_skill_default_format():
    result = subprocess.run(
        [sys.executable, "-m", "terrifying", "skill"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "package terrifying" in result.stdout


def test_cli_skill_unsupported_format():
    result = subprocess.run(
        [sys.executable, "-m", "terrifying", "skill", "--format", "cursor"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "not yet supported" in result.stdout
    assert ISSUES_URL in result.stdout

import subprocess
import sys


def test_textual_missing_exits_1(tmp_path, monkeypatch):
    # Simulate textual not being installed by patching the import
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.modules['textual'] = None\n"
            "from terrifying.cli import _cmd_add\n"
            "import argparse\n"
            "args = argparse.Namespace(policy_ids=[], engine='both', dry_run=False)\n"
            "try:\n"
            "    _cmd_add(args)\n"
            "except SystemExit as e:\n"
            "    sys.exit(e.code)\n",
        ],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.returncode == 1
    assert "textual" in result.stderr.lower() or "tui" in result.stderr.lower()

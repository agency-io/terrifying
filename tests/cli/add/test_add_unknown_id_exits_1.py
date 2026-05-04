import subprocess
import sys


def test_unknown_policy_id_exits_1(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "terrifying",
            "add",
            "nonexistent-policy-xyz-abc",
            "--engine",
            "rego",
        ],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.returncode == 1
    assert "nonexistent-policy-xyz-abc" in result.stderr

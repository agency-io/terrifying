"""Test that per-policy params are used when rendering a Jinja2 template."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.core.config import PolicyConfig
from terrifying.policies.c7n import C7nAdapter


def test_policy_params_override_in_template(tmp_path: Path) -> None:
    """Per-policy params override global params in Jinja2 rendering."""
    policy = tmp_path / "check_env.yml.j2"
    policy.write_text(
        "policies:\n  - name: check-{{ env }}\n    resource: terraform.aws_s3_bucket\n"
    )
    pc = PolicyConfig(
        path=tmp_path,
        params={"env": "prod"},
        policies={"check_env": {"params": {"env": "staging"}}},
    )
    adapter = C7nAdapter(pc)

    mock_result = MagicMock(stdout=json.dumps([]), returncode=0)
    written_content: list[str] = []

    def capture_run(cmd, **kwargs):
        policy_path = Path(cmd[cmd.index("--policy") + 1])
        written_content.append(policy_path.read_text(encoding="utf-8"))
        return mock_result

    with patch("terrifying.policies.c7n.subprocess.run", side_effect=capture_run):
        adapter.run(Path("/some/tf"))

    assert len(written_content) == 1
    assert "check-staging" in written_content[0]

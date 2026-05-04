"""Test that a Jinja2 template policy file is rendered before c7n-left is called."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.core.config import PolicyConfig
from terrifying.policies.c7n import C7nAdapter


def test_template_rendered_with_params(tmp_path: Path) -> None:
    """Jinja2 template is rendered with global params before invoking c7n-left."""
    policy = tmp_path / "require_tag.yml.j2"
    policy.write_text(
        "policies:\n"
        "{% for tag in required_tags %}\n"
        "  - name: require-{{ tag | lower }}-tag\n"
        "    resource: terraform.aws_s3_bucket\n"
        "    filters:\n"
        '      - "tag:{{ tag }}": absent\n'
        "{% endfor %}\n"
    )
    pc = PolicyConfig(path=tmp_path, params={"required_tags": ["Environment", "Team"]})
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
    rendered = written_content[0]
    assert "require-environment-tag" in rendered
    assert "require-team-tag" in rendered

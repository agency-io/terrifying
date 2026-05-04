"""Test that a plain YAML policy file passes through unchanged."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.policies.c7n import C7nAdapter


def test_plain_yml_no_params(tmp_path: Path) -> None:
    """A plain .yml file with no template markers passes through unchanged."""
    content = "policies:\n  - name: my-policy\n    resource: terraform.aws_s3_bucket\n"
    policy = tmp_path / "my_policy.yml"
    policy.write_text(content)
    adapter = C7nAdapter(tmp_path)

    mock_result = MagicMock(stdout=json.dumps([]), returncode=0)
    written_content: list[str] = []

    def capture_run(cmd, **kwargs):
        policy_path = Path(cmd[cmd.index("--policy") + 1])
        written_content.append(policy_path.read_text(encoding="utf-8"))
        return mock_result

    with patch("terrifying.policies.c7n.subprocess.run", side_effect=capture_run):
        adapter.run(Path("/some/tf"))

    assert len(written_content) == 1
    assert written_content[0] == content

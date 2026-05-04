import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ecs/ecs-task-definition-host-network-mode.yml"


def test_compliant():
    tf = tf_resource(
        "aws_ecs_task_definition", "main",
        '  network_mode             = "awsvpc"\n  container_definitions    = jsonencode([])\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_ecs_task_definition", "main",
        '  network_mode             = "host"\n  container_definitions    = jsonencode([])\n',
    )
    assert c7n_violations(POLICY, tf) != []

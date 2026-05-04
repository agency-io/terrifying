import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ecs/ecs-containers-readonly-access.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_ecs_task_definition",
        "main",
        '  container_definitions = jsonencode([{name="app", image="nginx", readonlyRootFilesystem=true}])\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_ecs_task_definition",
        "main",
        '  container_definitions = jsonencode([{name="app", image="nginx", readonlyRootFilesystem=false}])\n',
    )
    assert c7n_violations(POLICY, tf) != []

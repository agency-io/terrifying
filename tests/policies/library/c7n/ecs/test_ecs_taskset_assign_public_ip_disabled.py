import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ecs/ecs-taskset-assign-public-ip-disabled.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_ecs_service",
        "main",
        '  deployment_controller {\n    type = "EXTERNAL"\n  }\n  network_configuration {\n    assign_public_ip = false\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_ecs_service",
        "main",
        '  deployment_controller {\n    type = "EXTERNAL"\n  }\n  network_configuration {\n    assign_public_ip = true\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []


def test_non_external_compliant():
    tf = tf_resource(
        "aws_ecs_service",
        "main",
        '  deployment_controller {\n    type = "ECS"\n  }\n  network_configuration {\n    assign_public_ip = true\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []

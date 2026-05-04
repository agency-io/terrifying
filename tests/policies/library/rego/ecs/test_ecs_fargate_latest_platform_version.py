import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ecs/ecs-fargate-latest-platform-version.rego"


def test_compliant():
    inp = rego_input([resource("aws_ecs_service", "svc", {
        "launch_type": "FARGATE", "platform_version": "LATEST"
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_ecs_service", "svc", {
        "launch_type": "FARGATE", "platform_version": "1.3.0"
    })])
    assert eval_rego_policy(POLICY, inp) != []

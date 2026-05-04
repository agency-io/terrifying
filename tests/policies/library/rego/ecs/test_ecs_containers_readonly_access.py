import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ecs/ecs-containers-readonly-access.rego"


def test_compliant():
    inp = rego_input([resource("aws_ecs_task_definition", "app", {
        "container_definitions": '[{"name":"app","readonlyRootFilesystem":true}]'
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_ecs_task_definition", "app", {})])
    assert eval_rego_policy(POLICY, inp) != []

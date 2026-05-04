import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/secretsmanager/secretsmanager-rotation-enabled-check.rego"


def test_compliant():
    resources = [
        resource("aws_secretsmanager_secret", "mysecret", {}),
        resource("aws_secretsmanager_secret_rotation", "rot", {
            "secret_id": "mysecret",
            "rotation_rules": [{"automatically_after_days": 30}],
        }),
    ]
    inp = rego_input(resources)
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_secretsmanager_secret", "mysecret", {})])
    assert eval_rego_policy(POLICY, inp) != []

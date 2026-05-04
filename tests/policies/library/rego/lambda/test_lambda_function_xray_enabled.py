import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/lambda/lambda-function-xray-enabled.rego"


def test_compliant_active_tracing():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {
        "tracing_config": [{"mode": "Active"}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_passthrough():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {
        "tracing_config": [{"mode": "PassThrough"}],
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_no_tracing_config():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"function_name": "my_fn"})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_lambda_ignored():
    inp = rego_input([resource("aws_iam_role", "my_role", {})])
    assert eval_rego_policy(POLICY, inp) == []

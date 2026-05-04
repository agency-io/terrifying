import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/lambda/lambda-function-settings-check.rego"


def test_compliant_python311():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"runtime": "python3.11"})])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_nodejs20():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"runtime": "nodejs20.x"})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_python27():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"runtime": "python2.7"})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_nodejs12():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"runtime": "nodejs12.x"})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_go1x():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"runtime": "go1.x"})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_dotnetcore21():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"runtime": "dotnetcore2.1"})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_lambda_ignored():
    inp = rego_input([resource("aws_iam_role", "my_role", {"runtime": "python2.7"})])
    assert eval_rego_policy(POLICY, inp) == []

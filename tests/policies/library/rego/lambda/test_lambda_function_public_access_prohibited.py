import shutil
import json
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/lambda/lambda-function-public-access-prohibited.rego"


def test_compliant_specific_principal():
    policy_doc = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::123456789012:root"}, "Action": "lambda:InvokeFunction"}],
    })
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_no_policy():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"function_name": "my_fn"})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_wildcard_principal():
    policy_doc = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": "*", "Action": "lambda:InvokeFunction"}],
    })
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_wildcard_aws_principal():
    policy_doc = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"AWS": "*"}, "Action": "lambda:InvokeFunction"}],
    })
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_lambda_ignored():
    inp = rego_input([resource("aws_iam_policy", "my_policy", {})])
    assert eval_rego_policy(POLICY, inp) == []

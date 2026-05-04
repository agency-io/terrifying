import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/lambda/lambda-dlq-check.rego"


def test_compliant_with_dlq():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {
        "dead_letter_config": [{"target_arn": "arn:aws:sqs:us-east-1:123456789012:my-dlq"}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_no_dlq_config():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {"function_name": "my_fn"})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_empty_target_arn():
    inp = rego_input([resource("aws_lambda_function", "my_fn", {
        "dead_letter_config": [{"target_arn": ""}],
    })])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_lambda_ignored():
    inp = rego_input([resource("aws_iam_role", "my_role", {})])
    assert eval_rego_policy(POLICY, inp) == []

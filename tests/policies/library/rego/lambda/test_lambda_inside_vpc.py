import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/lambda/lambda-inside-vpc.rego"
)


def test_compliant_with_vpc():
    inp = rego_input(
        [
            resource(
                "aws_lambda_function",
                "my_fn",
                {
                    "vpc_config": [
                        {
                            "subnet_ids": ["subnet-aaa", "subnet-bbb"],
                            "security_group_ids": ["sg-aaa"],
                        }
                    ],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_no_vpc_config():
    inp = rego_input(
        [resource("aws_lambda_function", "my_fn", {"function_name": "my_fn"})]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_empty_subnets():
    inp = rego_input(
        [
            resource(
                "aws_lambda_function",
                "my_fn",
                {
                    "vpc_config": [{"subnet_ids": [], "security_group_ids": []}],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_non_lambda_ignored():
    inp = rego_input([resource("aws_iam_role", "my_role", {})])
    assert eval_rego_policy(POLICY, inp) == []

import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/lambda/lambda-vpc-multi-az-check.rego"
)


def test_compliant_two_subnets():
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


def test_compliant_three_subnets():
    inp = rego_input(
        [
            resource(
                "aws_lambda_function",
                "my_fn",
                {
                    "vpc_config": [
                        {
                            "subnet_ids": ["subnet-aaa", "subnet-bbb", "subnet-ccc"],
                            "security_group_ids": ["sg-aaa"],
                        }
                    ],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_no_vpc():
    # No vpc_config at all — not in VPC, single-AZ check doesn't apply
    inp = rego_input(
        [resource("aws_lambda_function", "my_fn", {"function_name": "my_fn"})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_one_subnet():
    inp = rego_input(
        [
            resource(
                "aws_lambda_function",
                "my_fn",
                {
                    "vpc_config": [
                        {"subnet_ids": ["subnet-aaa"], "security_group_ids": ["sg-aaa"]}
                    ],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_non_lambda_ignored():
    inp = rego_input([resource("aws_iam_role", "my_role", {})])
    assert eval_rego_policy(POLICY, inp) == []

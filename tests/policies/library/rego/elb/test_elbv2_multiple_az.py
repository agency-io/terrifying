import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elb/elbv2-multiple-az.rego"
)


def test_compliant_two_subnets():
    inp = rego_input(
        [
            resource(
                "aws_lb",
                "my_lb",
                {
                    "subnets": ["subnet-aaa", "subnet-bbb"],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_three_subnets():
    inp = rego_input(
        [
            resource(
                "aws_lb",
                "my_lb",
                {
                    "subnets": ["subnet-aaa", "subnet-bbb", "subnet-ccc"],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_one_subnet():
    inp = rego_input(
        [
            resource(
                "aws_lb",
                "my_lb",
                {
                    "subnets": ["subnet-aaa"],
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_non_alb_ignored():
    inp = rego_input([resource("aws_elb", "classic_lb", {"subnets": ["subnet-aaa"]})])
    assert eval_rego_policy(POLICY, inp) == []

import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elb/elb-deletion-protection-enabled.rego"
)


def test_compliant():
    inp = rego_input(
        [resource("aws_lb", "my_lb", {"enable_deletion_protection": True})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_disabled():
    inp = rego_input(
        [resource("aws_lb", "my_lb", {"enable_deletion_protection": False})]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_missing():
    inp = rego_input([resource("aws_lb", "my_lb", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_alb_ignored():
    inp = rego_input([resource("aws_elb", "classic_lb", {})])
    assert eval_rego_policy(POLICY, inp) == []

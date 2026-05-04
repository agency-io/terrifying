import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/autoscaling/autoscaling-group-elb-healthcheck-required.rego"


def test_compliant_elb_health_check():
    attrs = {"load_balancers": ["my-elb"], "target_group_arns": [], "health_check_type": "ELB"}
    inp = rego_input([resource("aws_autoscaling_group", "my_asg", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_no_load_balancer():
    attrs = {"load_balancers": [], "target_group_arns": [], "health_check_type": "EC2"}
    inp = rego_input([resource("aws_autoscaling_group", "my_asg", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    attrs = {"load_balancers": ["my-elb"], "target_group_arns": [], "health_check_type": "EC2"}
    inp = rego_input([resource("aws_autoscaling_group", "my_asg", attrs)])
    assert eval_rego_policy(POLICY, inp) != []

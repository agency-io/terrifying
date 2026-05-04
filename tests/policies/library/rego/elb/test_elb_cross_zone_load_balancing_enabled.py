import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elb/elb-cross-zone-load-balancing-enabled.rego"
)


def test_compliant():
    inp = rego_input(
        [resource("aws_elb", "classic_lb", {"cross_zone_load_balancing": True})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_disabled():
    inp = rego_input(
        [resource("aws_elb", "classic_lb", {"cross_zone_load_balancing": False})]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_missing():
    inp = rego_input([resource("aws_elb", "classic_lb", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_classic_elb_ignored():
    inp = rego_input([resource("aws_lb", "my_alb", {})])
    assert eval_rego_policy(POLICY, inp) == []

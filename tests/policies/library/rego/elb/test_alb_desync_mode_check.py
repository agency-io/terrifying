import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elb/alb-desync-mode-check.rego"
)


def test_compliant_defensive():
    inp = rego_input(
        [resource("aws_lb", "my_alb", {"desync_mitigation_mode": "defensive"})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_compliant_strictest():
    inp = rego_input(
        [resource("aws_lb", "my_alb", {"desync_mitigation_mode": "strictest"})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_monitor():
    inp = rego_input(
        [resource("aws_lb", "my_alb", {"desync_mitigation_mode": "monitor"})]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_non_alb_ignored():
    inp = rego_input(
        [resource("aws_elb", "classic_lb", {"desync_mitigation_mode": "monitor"})]
    )
    assert eval_rego_policy(POLICY, inp) == []

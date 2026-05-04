import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elb/alb-desync-mode-check.yml"


def test_compliant_defensive():
    tf = tf_resource("aws_lb", "my_lb", '  desync_mitigation_mode = "defensive"\n')
    assert c7n_violations(POLICY, tf) == []


def test_compliant_strictest():
    tf = tf_resource("aws_lb", "my_lb", '  desync_mitigation_mode = "strictest"\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource("aws_lb", "my_lb", '  desync_mitigation_mode = "monitor"\n')
    assert c7n_violations(POLICY, tf) != []

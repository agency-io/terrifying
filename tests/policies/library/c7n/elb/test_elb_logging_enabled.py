import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elb/elb-logging-enabled.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_lb",
        "my_lb",
        '  access_logs {\n    bucket = "my-bucket"\n    enabled = true\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource("aws_lb", "my_lb", '  name = "my-lb"\n')
    assert c7n_violations(POLICY, tf) != []

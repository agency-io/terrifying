import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/iam/iam-no-inline-policy-check.yml"
)


def test_compliant():
    # No aws_iam_user_policy resources means no violation
    tf = tf_resource("aws_iam_user", "my_user", '  name = "my-user"\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    # Any aws_iam_user_policy resource is a violation
    tf = tf_resource(
        "aws_iam_user_policy",
        "my_policy",
        '  name   = "my-inline-policy"\n  user   = "my-user"\n  policy = "{\\"Version\\":\\"2012-10-17\\",\\"Statement\\":[]}"\n',
    )
    assert c7n_violations(POLICY, tf) != []

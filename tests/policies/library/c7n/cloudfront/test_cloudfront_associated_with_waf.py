import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/cloudfront/cloudfront-associated-with-waf.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_cloudfront_distribution",
        "dist",
        '  web_acl_id = "arn:aws:wafv2:us-east-1:123:global/webacl/my-acl/abc"\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource("aws_cloudfront_distribution", "dist", "  enabled = true\n")
    assert c7n_violations(POLICY, tf) != []

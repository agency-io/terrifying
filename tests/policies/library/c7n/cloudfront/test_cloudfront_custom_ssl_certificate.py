import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/cloudfront/cloudfront-custom-ssl-certificate.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_cloudfront_distribution",
        "dist",
        '  viewer_certificate {\n    acm_certificate_arn = "arn:aws:acm:us-east-1:123:certificate/abc"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_cloudfront_distribution",
        "dist",
        "  viewer_certificate {\n    cloudfront_default_certificate = true\n  }\n",
    )
    assert c7n_violations(POLICY, tf) != []

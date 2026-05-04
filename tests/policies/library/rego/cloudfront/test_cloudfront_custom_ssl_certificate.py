import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/cloudfront/cloudfront-custom-ssl-certificate.rego"
)


def test_compliant():
    attrs = {
        "viewer_certificate": [
            {
                "cloudfront_default_certificate": False,
                "acm_certificate_arn": "arn:aws:acm:us-east-1:123:certificate/abc",
            }
        ]
    }
    inp = rego_input([resource("aws_cloudfront_distribution", "my_cf", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    attrs = {"viewer_certificate": [{"cloudfront_default_certificate": True}]}
    inp = rego_input([resource("aws_cloudfront_distribution", "my_cf", attrs)])
    assert eval_rego_policy(POLICY, inp) != []

import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/cloudfront/cloudfront-s3-origin-access-control-enabled.rego"


def test_compliant():
    attrs = {"origin": [{"domain_name": "mybucket.s3.us-east-1.amazonaws.com", "origin_access_control_id": "ABCDEF123456"}]}
    inp = rego_input([resource("aws_cloudfront_distribution", "my_cf", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    attrs = {"origin": [{"domain_name": "mybucket.s3.us-east-1.amazonaws.com", "origin_access_control_id": ""}]}
    inp = rego_input([resource("aws_cloudfront_distribution", "my_cf", attrs)])
    assert eval_rego_policy(POLICY, inp) != []

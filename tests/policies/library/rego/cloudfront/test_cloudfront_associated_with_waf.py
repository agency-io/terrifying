import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/cloudfront/cloudfront-associated-with-waf.rego"


def test_compliant():
    inp = rego_input([resource("aws_cloudfront_distribution", "my_cf", {"web_acl_id": "arn:aws:wafv2:us-east-1:123:global/webacl/example/abc"})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_cloudfront_distribution", "my_cf", {})])
    assert eval_rego_policy(POLICY, inp) != []

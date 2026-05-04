import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/cloudfront/cloudfront-origin-failover-enabled.rego"
)


def test_compliant():
    attrs = {
        "origin_group": [
            {
                "origin_id": "my-group",
                "failover_criteria": [
                    {"status_codes": [{"items": [500], "quantity": 1}]}
                ],
                "member": [],
            }
        ]
    }
    inp = rego_input([resource("aws_cloudfront_distribution", "my_cf", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_cloudfront_distribution", "my_cf", {})])
    assert eval_rego_policy(POLICY, inp) != []

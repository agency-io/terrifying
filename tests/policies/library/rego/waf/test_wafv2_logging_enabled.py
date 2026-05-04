import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/waf/wafv2-logging-enabled.rego"


def test_compliant():
    resources = [
        resource("aws_wafv2_web_acl", "acl", {"name": "my-acl"}),
        resource("aws_wafv2_web_acl_logging_configuration", "log", {
            "resource_arn": "acl",
            "log_destination_configs": ["arn:aws:firehose:us-east-1:123:deliverystream/my-stream"],
        }),
    ]
    inp = rego_input(resources)
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_wafv2_web_acl", "acl", {"name": "my-acl"})])
    assert eval_rego_policy(POLICY, inp) != []

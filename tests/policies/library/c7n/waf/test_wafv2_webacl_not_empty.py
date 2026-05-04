import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/waf/wafv2-webacl-not-empty.yml"


def test_compliant():
    tf = tf_resource(
        "aws_wafv2_web_acl", "acl",
        '  name  = "my-acl"\n  scope = "REGIONAL"\n  default_action {\n    allow {}\n  }\n  rule {\n    name     = "my-rule"\n    priority = 1\n    action {\n      block {}\n    }\n    visibility_config {\n      cloudwatch_metrics_enabled = true\n      metric_name                = "my-rule"\n      sampled_requests_enabled   = true\n    }\n    statement {\n      ip_set_reference_statement {\n        arn = "arn:aws:wafv2:::regional/ipset/my-ip-set"\n      }\n    }\n  }\n  visibility_config {\n    cloudwatch_metrics_enabled = true\n    metric_name                = "my-acl"\n    sampled_requests_enabled   = true\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_wafv2_web_acl", "acl",
        '  name  = "my-acl"\n  scope = "REGIONAL"\n  rule  = []\n  default_action {\n    allow {}\n  }\n  visibility_config {\n    cloudwatch_metrics_enabled = true\n    metric_name                = "my-acl"\n    sampled_requests_enabled   = true\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []

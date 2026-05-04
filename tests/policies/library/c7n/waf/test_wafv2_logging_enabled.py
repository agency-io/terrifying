import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/waf/wafv2-logging-enabled.yml"


def test_compliant_no_logging_resource():
    # Policy targets aws_wafv2_web_acl_logging_configuration.
    # A plain WAF ACL without the logging resource yields no violations on that type.
    tf = tf_resource(
        "aws_wafv2_web_acl", "acl",
        '  name  = "my-acl"\n  scope = "REGIONAL"\n  default_action {\n    allow {}\n  }\n  visibility_config {\n    cloudwatch_metrics_enabled = true\n    metric_name                = "my-acl"\n    sampled_requests_enabled   = true\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation_logging_resource_exists():
    # The logging config resource existing is matched (empty filters flag all).
    tf = tf_resource(
        "aws_wafv2_web_acl_logging_configuration", "logging",
        '  log_destination_configs = ["arn:aws:firehose:::deliverystream/my-stream"]\n  resource_arn            = "arn:aws:wafv2:::regional/webacl/my-acl"\n',
    )
    assert c7n_violations(POLICY, tf) != []

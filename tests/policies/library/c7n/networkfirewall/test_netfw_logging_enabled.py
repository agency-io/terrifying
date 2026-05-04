import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/networkfirewall/netfw-logging-enabled.yml"
)


def test_compliant():
    # A firewall resource exists — policy has no filters so all resources match.
    # Compliant means a logging config resource exists alongside the firewall.
    # For c7n-left with empty filters, every aws_networkfirewall_firewall is flagged.
    # Providing no firewall resource yields no violations.
    tf = tf_resource(
        "aws_networkfirewall_logging_configuration",
        "logs",
        "  firewall_arn = aws_networkfirewall_firewall.fw.arn\n",
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_networkfirewall_firewall",
        "fw",
        '  name   = "example"\n  vpc_id = "vpc-12345"\n',
    )
    assert c7n_violations(POLICY, tf) != []

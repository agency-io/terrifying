import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elasticsearch/opensearch-audit-logging-enabled.rego"


def test_compliant():
    inp = rego_input([resource("aws_opensearch_domain", "os", {
        "log_publishing_options": [{"log_type": "AUDIT_LOGS", "enabled": True, "cloudwatch_log_group_arn": "arn:aws:logs:us-east-1:123:log-group:os"}]
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_opensearch_domain", "os", {"log_publishing_options": []})])
    assert eval_rego_policy(POLICY, inp) != []

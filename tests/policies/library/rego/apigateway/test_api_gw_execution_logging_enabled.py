import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/apigateway/api-gw-execution-logging-enabled.rego"


def test_compliant():
    attrs = {"access_log_settings": [{"destination_arn": "arn:aws:logs:us-east-1:123:log-group:example"}]}
    inp = rego_input([resource("aws_api_gateway_stage", "my_stage", attrs)])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_api_gateway_stage", "my_stage", {})])
    assert eval_rego_policy(POLICY, inp) != []

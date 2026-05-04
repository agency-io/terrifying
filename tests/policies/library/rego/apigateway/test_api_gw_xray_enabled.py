import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/apigateway/api-gw-xray-enabled.rego"


def test_compliant():
    inp = rego_input([resource("aws_api_gateway_stage", "my_stage", {"xray_tracing_enabled": True})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_api_gateway_stage", "my_stage", {"xray_tracing_enabled": False})])
    assert eval_rego_policy(POLICY, inp) != []

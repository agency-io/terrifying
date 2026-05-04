import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/apigateway/api-gw-cache-encrypted.rego"
)


def test_compliant_cache_disabled():
    inp = rego_input(
        [
            resource(
                "aws_api_gateway_stage", "my_stage", {"cache_cluster_enabled": False}
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_cache_enabled_not_encrypted():
    attrs = {
        "cache_cluster_enabled": True,
        "method_settings": [{"cache_data_encrypted": False}],
    }
    inp = rego_input([resource("aws_api_gateway_stage", "my_stage", attrs)])
    assert eval_rego_policy(POLICY, inp) != []


def test_compliant_cache_enabled_encrypted():
    attrs = {
        "cache_cluster_enabled": True,
        "method_settings": [{"cache_data_encrypted": True}],
    }
    inp = rego_input([resource("aws_api_gateway_stage", "my_stage", attrs)])
    assert eval_rego_policy(POLICY, inp) == []

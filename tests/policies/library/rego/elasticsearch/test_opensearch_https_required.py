import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/elasticsearch/opensearch-https-required.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_opensearch_domain",
                "os",
                {"domain_endpoint_options": [{"enforce_https": True}]},
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input(
        [
            resource(
                "aws_opensearch_domain",
                "os",
                {"domain_endpoint_options": [{"enforce_https": False}]},
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []

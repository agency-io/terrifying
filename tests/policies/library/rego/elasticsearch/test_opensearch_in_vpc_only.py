import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elasticsearch/opensearch-in-vpc-only.rego"


def test_compliant():
    inp = rego_input([resource("aws_opensearch_domain", "os", {
        "vpc_options": [{"subnet_ids": ["subnet-abc"]}]
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_opensearch_domain", "os", {})])
    assert eval_rego_policy(POLICY, inp) != []

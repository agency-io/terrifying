import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/redshift/redshift-cluster-audit-logging-enabled.rego"


def test_compliant():
    inp = rego_input([resource("aws_redshift_cluster", "cluster", {
        "logging": [{"enable": True, "bucket_name": "my-logs"}],
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_redshift_cluster", "cluster", {
        "logging": [{"enable": False}],
    })])
    assert eval_rego_policy(POLICY, inp) != []

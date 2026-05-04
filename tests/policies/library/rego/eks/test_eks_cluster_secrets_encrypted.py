import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/eks/eks-cluster-secrets-encrypted.rego"


def test_compliant():
    inp = rego_input([resource("aws_eks_cluster", "cluster", {
        "encryption_config": [{"resources": ["secrets"], "provider": {"key_arn": "arn:aws:kms:us-east-1:123:key/abc"}}]
    })])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input([resource("aws_eks_cluster", "cluster", {
        "encryption_config": [{"resources": ["configmaps"], "provider": {"key_arn": "arn:aws:kms:us-east-1:123:key/abc"}}]
    })])
    assert eval_rego_policy(POLICY, inp) != []

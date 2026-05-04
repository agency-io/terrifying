import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/eks/eks-cluster-secrets-encrypted.yml"


def test_compliant():
    tf = tf_resource(
        "aws_eks_cluster", "main",
        '  encryption_config {\n    resources = ["secrets"]\n    provider {\n      key_arn = "arn:aws:kms:us-east-1:123456789012:key/abc"\n    }\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_eks_cluster", "main",
        '  name = "my-cluster"\n',
    )
    assert c7n_violations(POLICY, tf) != []

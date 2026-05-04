import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/ecr/ecr-private-repo-kms-encrypted.yml"


def test_compliant():
    tf = tf_resource("aws_ecr_repository", "repo", '  encryption_configuration {\n    encryption_type = "KMS"\n    kms_key = "arn:aws:kms:us-east-1:123:key/abc"\n  }\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource("aws_ecr_repository", "repo", '  encryption_configuration {\n    encryption_type = "AES256"\n  }\n')
    assert c7n_violations(POLICY, tf) != []

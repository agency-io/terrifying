import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ecr/ecr-private-repo-kms-encrypted.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_ecr_repository",
                "repo",
                {
                    "encryption_configuration": [
                        {
                            "encryption_type": "KMS",
                            "kms_key": "arn:aws:kms:us-east-1:123:key/abc",
                        }
                    ]
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation():
    inp = rego_input(
        [
            resource(
                "aws_ecr_repository",
                "repo",
                {
                    "encryption_configuration": [
                        {"encryption_type": "AES256", "kms_key": ""}
                    ]
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []

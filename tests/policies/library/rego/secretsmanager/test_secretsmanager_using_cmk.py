import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/secretsmanager/secretsmanager-using-cmk.rego"
)


def test_compliant():
    inp = rego_input(
        [
            resource(
                "aws_secretsmanager_secret",
                "secret",
                {
                    "kms_key_id": "arn:aws:kms:us-east-1:123456789012:key/my-cmk",
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_no_kms():
    inp = rego_input([resource("aws_secretsmanager_secret", "secret", {})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_default_key():
    inp = rego_input(
        [
            resource(
                "aws_secretsmanager_secret",
                "secret",
                {
                    "kms_key_id": "alias/aws/secretsmanager",
                },
            )
        ]
    )
    assert eval_rego_policy(POLICY, inp) != []

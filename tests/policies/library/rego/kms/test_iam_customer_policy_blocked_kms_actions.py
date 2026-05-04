import shutil
import json
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/kms/iam-customer-policy-blocked-kms-actions.rego"
)


def test_compliant_scoped_kms_decrypt():
    policy_doc = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["kms:Decrypt"],
                    "Resource": ["arn:aws:kms:us-east-1:123:key/abc"],
                }
            ],
        }
    )
    inp = rego_input([resource("aws_iam_policy", "my_policy", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_kms_decrypt_all_resources():
    policy_doc = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {"Effect": "Allow", "Action": ["kms:Decrypt"], "Resource": ["*"]}
            ],
        }
    )
    inp = rego_input([resource("aws_iam_policy", "my_policy", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_kms_reencryptfrom_all_resources():
    policy_doc = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {"Effect": "Allow", "Action": ["kms:ReEncryptFrom"], "Resource": ["*"]}
            ],
        }
    )
    inp = rego_input([resource("aws_iam_policy", "my_policy", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) != []


def test_compliant_deny_statement():
    policy_doc = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {"Effect": "Deny", "Action": ["kms:Decrypt"], "Resource": ["*"]}
            ],
        }
    )
    inp = rego_input([resource("aws_iam_policy", "my_policy", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) == []


def test_non_iam_policy_ignored():
    inp = rego_input([resource("aws_kms_key", "my_key", {})])
    assert eval_rego_policy(POLICY, inp) == []

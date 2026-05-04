import shutil
import json
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/kms/kms-key-policy-no-public-access.rego"
)


def test_compliant_specific_principal():
    policy_doc = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "arn:aws:iam::123456789012:root"},
                    "Action": "kms:*",
                    "Resource": "*",
                }
            ],
        }
    )
    inp = rego_input([resource("aws_kms_key", "my_key", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_wildcard_principal_string():
    policy_doc = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "kms:*",
                    "Resource": "*",
                }
            ],
        }
    )
    inp = rego_input([resource("aws_kms_key", "my_key", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_wildcard_principal_aws():
    policy_doc = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": "kms:*",
                    "Resource": "*",
                }
            ],
        }
    )
    inp = rego_input([resource("aws_kms_key", "my_key", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) != []


def test_non_kms_key_ignored():
    inp = rego_input([resource("aws_iam_policy", "my_policy", {})])
    assert eval_rego_policy(POLICY, inp) == []

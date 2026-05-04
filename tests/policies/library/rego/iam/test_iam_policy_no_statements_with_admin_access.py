import shutil
import json
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(
    not shutil.which("opa"), reason="opa not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/iam/iam-policy-no-statements-with-admin-access.rego"


def test_compliant_restricted_policy():
    policy_doc = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": ["arn:aws:s3:::my-bucket/*"]}],
    })
    inp = rego_input([resource("aws_iam_policy", "my_policy", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_admin_access_string():
    policy_doc = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}],
    })
    inp = rego_input([resource("aws_iam_policy", "my_policy", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) != []


def test_violation_admin_access_array():
    policy_doc = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Action": ["*"], "Resource": ["*"]}],
    })
    inp = rego_input([resource("aws_iam_policy", "my_policy", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) != []


def test_compliant_deny_statement():
    policy_doc = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*"}],
    })
    inp = rego_input([resource("aws_iam_policy", "my_policy", {"policy": policy_doc})])
    assert eval_rego_policy(POLICY, inp) == []


def test_non_iam_policy_ignored():
    inp = rego_input([resource("aws_iam_user", "my_user", {})])
    assert eval_rego_policy(POLICY, inp) == []

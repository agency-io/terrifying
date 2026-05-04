import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import eval_rego_policy, rego_input, resource

pytestmark = pytest.mark.skipif(not shutil.which("opa"), reason="opa not on PATH")

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/rds/rds-snapshots-public-prohibited.rego"
)


def test_compliant_instance_snapshot():
    inp = rego_input([resource("aws_db_snapshot", "snap", {"shared_accounts": []})])
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_instance_snapshot():
    inp = rego_input(
        [resource("aws_db_snapshot", "snap", {"shared_accounts": ["all"]})]
    )
    assert eval_rego_policy(POLICY, inp) != []


def test_compliant_cluster_snapshot():
    inp = rego_input(
        [resource("aws_db_cluster_snapshot", "snap", {"shared_accounts": []})]
    )
    assert eval_rego_policy(POLICY, inp) == []


def test_violation_cluster_snapshot():
    inp = rego_input(
        [resource("aws_db_cluster_snapshot", "snap", {"shared_accounts": ["all"]})]
    )
    assert eval_rego_policy(POLICY, inp) != []

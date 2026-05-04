import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/secretsmanager/secretsmanager-rotation-enabled-check.yml"
)


def test_compliant_no_rotation_resource():
    # Policy targets aws_secretsmanager_secret_rotation (empty filters).
    # A plain secret without the rotation resource yields no violations.
    tf = tf_resource("aws_secretsmanager_secret", "secret", '  name = "my-secret"\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation_rotation_resource_exists():
    # The rotation resource existing means it is matched (empty filters flag all).
    tf = tf_resource(
        "aws_secretsmanager_secret_rotation",
        "rotation",
        '  secret_id           = "my-secret"\n  rotation_lambda_arn = "arn:aws:lambda:::function:rotate"\n',
    )
    assert c7n_violations(POLICY, tf) != []

import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/kms/cmk-backing-key-rotation-enabled.yml"


def test_compliant():
    tf = tf_resource("aws_kms_key", "my_key", '  enable_key_rotation = true\n')
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource("aws_kms_key", "my_key", '  enable_key_rotation = false\n')
    assert c7n_violations(POLICY, tf) != []

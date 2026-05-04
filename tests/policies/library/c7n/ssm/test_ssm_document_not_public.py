import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "terrifying/policies/library/ssm/ssm-document-not-public.yml"
)


def test_compliant():
    tf = tf_resource(
        "aws_ssm_document",
        "doc",
        '  name          = "my-doc"\n  document_type = "Command"\n  permissions = {\n    account_ids = "123456789012"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_ssm_document",
        "doc",
        '  name          = "my-doc"\n  document_type = "Command"\n  permissions = {\n    account_ids = "all"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []

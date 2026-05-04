import shutil
from pathlib import Path
import pytest
from tests.policies.library.helpers import c7n_violations, tf_resource

pytestmark = pytest.mark.skipif(
    not shutil.which("c7n-left"), reason="c7n-left not on PATH"
)

POLICY = Path(__file__).parent.parent.parent.parent.parent.parent / "terrifying/policies/library/elasticbeanstalk/beanstalk-enhanced-health-reporting-enabled.yml"


def test_compliant():
    tf = tf_resource(
        "aws_elastic_beanstalk_environment", "main",
        '  setting {\n    namespace = "aws:elasticbeanstalk:healthreporting:system"\n    name      = "SystemType"\n    value     = "enhanced"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) == []


def test_violation():
    tf = tf_resource(
        "aws_elastic_beanstalk_environment", "main",
        '  setting {\n    namespace = "aws:elasticbeanstalk:healthreporting:system"\n    name      = "SystemType"\n    value     = "basic"\n  }\n',
    )
    assert c7n_violations(POLICY, tf) != []

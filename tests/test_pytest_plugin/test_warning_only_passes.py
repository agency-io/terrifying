"""Test that warning-severity violations do not cause the test item to fail."""

pytest_plugins = ["pytester"]

_TF_RESOURCE = """
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
}
"""


def test_warning_only_passes(pytester):
    """Items with only warning-severity violations should pass."""
    pytester.makefile(
        ".yml",
        terrifying="""
rules:
  required_tags:
    tags:
      - Environment
terraform:
  path: ./terraform
""",
    )
    pytester.mkdir("terraform")
    # Write a conftest that patches the violation severity to warning
    pytester.makeconftest("""
import terrifying.rules.best_practices as bp
import terrifying.core.rule as rule_mod

_orig_check = bp.RequiredTags.check

def _warning_check(self, context):
    violations = _orig_check(self, context)
    for v in violations:
        v.severity = "warning"
    return violations

bp.RequiredTags.check = _warning_check
""")
    pytester.makefile(".tf", **{"terraform/main": _TF_RESOURCE})
    result = pytester.runpytest("-v")
    result.assert_outcomes(passed=1)

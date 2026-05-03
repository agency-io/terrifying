"""Test that a rule with error-severity violations produces a failing test item."""

pytest_plugins = ["pytester"]

_TF_MANY_RESOURCES = """
resource "aws_s3_bucket" "a" {}
resource "aws_s3_bucket" "b" {}
resource "aws_s3_bucket" "c" {}
"""


def test_rule_fails_with_violations(pytester):
    """A rule that finds error-severity violations should fail."""
    pytester.makefile(
        ".yml",
        terrifying="""
rules:
  max_resources_per_file:
    max_resources: 1
terraform:
  path: ./terraform
""",
    )
    pytester.mkdir("terraform")
    pytester.makefile(".tf", **{"terraform/main": _TF_MANY_RESOURCES})
    result = pytester.runpytest("-v")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*max_resources_per_file*"])

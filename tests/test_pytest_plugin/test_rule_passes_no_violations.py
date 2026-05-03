"""Test that a rule with no violations produces a passing test item."""

pytest_plugins = ["pytester"]


def test_rule_passes_no_violations(pytester):
    """A rule that finds no violations should pass."""
    pytester.makefile(
        ".yml",
        terrifying="""
rules:
  max_resources_per_file:
    max_resources: 10
terraform:
  path: ./terraform
""",
    )
    pytester.mkdir("terraform")
    pytester.makefile(".tf", **{"terraform/empty": ""})
    result = pytester.runpytest("-v")
    result.assert_outcomes(passed=1)

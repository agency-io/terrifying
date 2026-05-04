"""Test that one TerraformCheckItem is yielded for each enabled rule."""

pytest_plugins = ["pytester"]


def test_collects_one_item_per_rule(pytester):
    """Each rule in terrifying.yml produces exactly one test item."""
    pytester.makefile(
        ".yml",
        terrifying="""
rules:
  max_resources_per_file:
    max_resources: 10
  max_lines_per_file:
    max_lines: 100
terraform:
  path: ./terraform
""",
    )
    pytester.mkdir("terraform")
    pytester.makefile(".tf", **{"terraform/empty": ""})
    result = pytester.runpytest("-v")
    result.assert_outcomes(passed=2)

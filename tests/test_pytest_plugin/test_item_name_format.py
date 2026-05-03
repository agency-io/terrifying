"""Test that TerraformCheckItem node IDs use the terrifying::<rule_id> format."""

pytest_plugins = ["pytester"]


def test_item_name_format(pytester):
    """Test item node IDs should be in the form terrifying::<rule_id>."""
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
    result.stdout.fnmatch_lines(["*terrifying::max_resources_per_file*"])

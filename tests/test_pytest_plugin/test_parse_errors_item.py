"""Test that parse errors produce a dedicated parse_errors test item."""

pytest_plugins = ["pytester"]


def test_parse_errors_item(pytester):
    """An unparseable .tf file should yield a failing parse_errors item."""
    pytester.makefile(
        ".yml",
        terrifying="""
rules: {}
terraform:
  path: ./terraform
""",
    )
    pytester.mkdir("terraform")
    pytester.makefile(".tf", **{"terraform/broken": "this is not valid hcl {"})
    result = pytester.runpytest("-v")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*parse_errors*"])

"""Test that terraform.path in terrifying.yml is used to locate .tf files."""

pytest_plugins = ["pytester"]

_TF_MANY_RESOURCES = """
resource "aws_s3_bucket" "a" {}
resource "aws_s3_bucket" "b" {}
resource "aws_s3_bucket" "c" {}
"""


def test_terraform_path_config(pytester):
    """terraform.path points the collector to the right subdirectory."""
    pytester.makefile(
        ".yml",
        terrifying="""
rules:
  max_resources_per_file:
    max_resources: 1
terraform:
  path: ./infra
""",
    )
    pytester.mkdir("infra")
    pytester.makefile(".tf", **{"infra/main": _TF_MANY_RESOURCES})
    result = pytester.runpytest("-v")
    result.assert_outcomes(failed=1)

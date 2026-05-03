from pathlib import Path
from unittest.mock import patch

import pytest

from terrifying.core.parser import Parser


@pytest.fixture
def parser() -> Parser:
    return Parser()


# ── Valid directory parsing ───────────────────────────────────────────────────


def test_parse_valid_resources(parser, tmp_path):
    (tmp_path / "main.tf").write_text(
        'resource "aws_s3_bucket" "one" { bucket = "x" }\n'
        'resource "aws_s3_bucket" "two" { bucket = "y" }\n'
    )
    ctx = parser.parse_directory(tmp_path)
    assert len(ctx.files) == 1
    assert len(ctx.resources) == 2
    assert ctx.parse_violations == []


def test_parse_resource_fields(parser, tmp_path):
    (tmp_path / "main.tf").write_text(
        'resource "aws_instance" "web" { ami = "ami-123" }\n'
    )
    ctx = parser.parse_directory(tmp_path)
    r = ctx.resources[0]
    assert r.type == "aws_instance"
    assert r.name == "web"
    assert r.file == tmp_path / "main.tf"


def test_parse_variables(parser, fixtures_dir):
    ctx = parser.parse_directory(fixtures_dir)
    all_vars = [v for f in ctx.files for v in f.variables]
    var = next(v for v in all_vars if v.name == "region")
    assert var.description == "AWS region"
    assert var.default == "us-east-1"


def test_parse_outputs(parser, fixtures_dir):
    ctx = parser.parse_directory(fixtures_dir)
    all_outputs = [o for f in ctx.files for o in f.outputs]
    out = next(o for o in all_outputs if o.name == "bucket_arn")
    assert out.description == "The bucket ARN"


def test_parse_locals(parser, fixtures_dir):
    ctx = parser.parse_directory(fixtures_dir)
    all_locals = [loc for f in ctx.files for loc in f.locals]
    local = next(loc for loc in all_locals if loc.name == "env")
    assert local.value == "prod"


def test_parse_module_calls(parser, fixtures_dir):
    ctx = parser.parse_directory(fixtures_dir)
    all_modules = [m for f in ctx.files for m in f.module_calls]
    mod = next(m for m in all_modules if m.name == "vpc")
    assert mod.source == "terraform-aws-modules/vpc/aws"


def test_parse_line_count(parser, fixtures_dir):
    ctx = parser.parse_directory(fixtures_dir)
    for tf_file in ctx.files:
        expected = len(tf_file.path.read_text().splitlines())
        assert tf_file.line_count == expected


def test_parse_multiple_files(parser, tmp_path):
    (tmp_path / "a.tf").write_text('resource "aws_s3_bucket" "one" { bucket = "x" }\n')
    (tmp_path / "b.tf").write_text('resource "aws_s3_bucket" "two" { bucket = "y" }\n')
    ctx = parser.parse_directory(tmp_path)
    assert len(ctx.files) == 2
    assert len(ctx.resources) == 2


# ── Non-dict attrs (defensive guards) ────────────────────────────────────────


def test_resource_non_dict_attrs_treated_as_empty(parser, tmp_path):
    (tmp_path / "main.tf").write_text("")
    malformed = {"resource": [{"aws_s3_bucket": {"my_bucket": "not_a_dict"}}]}
    with patch("terrifying.core.parser.hcl2.load", return_value=malformed):
        ctx = parser.parse_directory(tmp_path)
    assert len(ctx.resources) == 1
    assert ctx.resources[0].attributes == {}


def test_variable_non_dict_attrs_treated_as_empty(parser, tmp_path):
    (tmp_path / "main.tf").write_text("")
    malformed = {"variable": [{"region": "not_a_dict"}]}
    with patch("terrifying.core.parser.hcl2.load", return_value=malformed):
        ctx = parser.parse_directory(tmp_path)
    all_vars = [v for f in ctx.files for v in f.variables]
    assert len(all_vars) == 1
    assert all_vars[0].description is None


def test_output_non_dict_attrs_treated_as_empty(parser, tmp_path):
    (tmp_path / "main.tf").write_text("")
    malformed = {"output": [{"bucket_arn": "not_a_dict"}]}
    with patch("terrifying.core.parser.hcl2.load", return_value=malformed):
        ctx = parser.parse_directory(tmp_path)
    all_outputs = [o for f in ctx.files for o in f.outputs]
    assert len(all_outputs) == 1
    assert all_outputs[0].value is None


def test_module_non_dict_attrs_treated_as_empty(parser, tmp_path):
    (tmp_path / "main.tf").write_text("")
    malformed = {"module": [{"vpc": "not_a_dict"}]}
    with patch("terrifying.core.parser.hcl2.load", return_value=malformed):
        ctx = parser.parse_directory(tmp_path)
    all_modules = [m for f in ctx.files for m in f.module_calls]
    assert len(all_modules) == 1
    assert all_modules[0].source == ""
    assert all_modules[0].arguments == {}


def test_resource_list_attr_is_stripped_recursively(parser, tmp_path):
    (tmp_path / "main.tf").write_text("")
    data = {"resource": [{"aws_security_group": {"sg": {"ingress": ['"0.0.0.0/0"', '"10.0.0.0/8"']}}}]}
    with patch("terrifying.core.parser.hcl2.load", return_value=data):
        ctx = parser.parse_directory(tmp_path)
    assert ctx.resources[0].attributes["ingress"] == ["0.0.0.0/0", "10.0.0.0/8"]


def test_locals_non_dict_block_is_skipped(parser, tmp_path):
    (tmp_path / "main.tf").write_text("")
    data = {"locals": ["not_a_dict"]}
    with patch("terrifying.core.parser.hcl2.load", return_value=data):
        ctx = parser.parse_directory(tmp_path)
    all_locals = [loc for f in ctx.files for loc in f.locals]
    assert all_locals == []


# ── Invalid HCL ───────────────────────────────────────────────────────────────


def test_invalid_hcl_produces_parse_error_violation(parser, tmp_path):
    (tmp_path / "invalid.tf").write_text("this is not valid terraform !!!\n")
    ctx = parser.parse_directory(tmp_path)
    assert len(ctx.parse_violations) == 1
    assert ctx.parse_violations[0].rule == "parse_error"
    assert ctx.parse_violations[0].severity == "error"


def test_invalid_hcl_file_omitted_from_files(parser, tmp_path):
    (tmp_path / "invalid.tf").write_text("this is not valid terraform !!!\n")
    ctx = parser.parse_directory(tmp_path)
    assert ctx.files == []


def test_invalid_hcl_does_not_stop_other_files(parser, tmp_path):
    (tmp_path / "invalid.tf").write_text("this is not valid terraform !!!\n")
    (tmp_path / "valid.tf").write_text('resource "aws_s3_bucket" "ok" { bucket = "x" }\n')
    ctx = parser.parse_directory(tmp_path)
    assert len(ctx.parse_violations) == 1
    assert len(ctx.files) == 1
    assert len(ctx.resources) == 1


def test_parse_violation_names_the_file(parser, tmp_path):
    (tmp_path / "broken.tf").write_text("not valid\n")
    ctx = parser.parse_directory(tmp_path)
    assert "broken.tf" in ctx.parse_violations[0].message


# ── Edge cases ────────────────────────────────────────────────────────────────


def test_empty_directory(parser, tmp_path):
    ctx = parser.parse_directory(tmp_path)
    assert ctx.files == []
    assert ctx.resources == []
    assert ctx.parse_violations == []


def test_directory_with_no_tf_files(parser, tmp_path):
    (tmp_path / "README.md").write_text("# hello\n")
    (tmp_path / "main.py").write_text("x = 1\n")
    ctx = parser.parse_directory(tmp_path)
    assert ctx.files == []
    assert ctx.resources == []


def test_non_tf_files_are_ignored(parser, tmp_path):
    (tmp_path / "main.tf").write_text('resource "aws_s3_bucket" "ok" { bucket = "x" }\n')
    (tmp_path / "vars.tfvars").write_text('region = "us-east-1"\n')
    ctx = parser.parse_directory(tmp_path)
    assert len(ctx.files) == 1


def test_parse_violation_file_path_set(parser, tmp_path):
    broken = tmp_path / "broken.tf"
    broken.write_text("not valid\n")
    ctx = parser.parse_directory(tmp_path)
    assert ctx.parse_violations[0].file == broken

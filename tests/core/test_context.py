from pathlib import Path

from terrifying.core.context import (
    Local,
    ModuleCall,
    Output,
    Resource,
    TerraformContext,
    TerraformFile,
    Variable,
    _file_to_dict,
    _output_to_dict,
    _resource_to_dict,
    _variable_to_dict,
)


def _make_resource(name: str = "bucket", path: Path = Path("main.tf")) -> Resource:
    return Resource(
        type="aws_s3_bucket", name=name, attributes={"bucket": "x"}, file=path
    )


def _make_file(path: Path, resources: list[Resource] | None = None) -> TerraformFile:
    return TerraformFile(
        path=path,
        resources=resources or [],
        line_count=10,
    )


# ── TerraformContext.resources ────────────────────────────────────────────────


def test_resources_empty_context():
    ctx = TerraformContext()
    assert ctx.resources == []


def test_resources_single_file():
    r = _make_resource()
    f = _make_file(Path("main.tf"), [r])
    ctx = TerraformContext(files=[f])
    assert ctx.resources == [r]


def test_resources_flat_across_multiple_files():
    r1 = _make_resource("one", Path("a.tf"))
    r2 = _make_resource("two", Path("b.tf"))
    ctx = TerraformContext(
        files=[
            _make_file(Path("a.tf"), [r1]),
            _make_file(Path("b.tf"), [r2]),
        ]
    )
    assert ctx.resources == [r1, r2]


def test_resources_multiple_per_file():
    r1 = _make_resource("one")
    r2 = _make_resource("two")
    ctx = TerraformContext(files=[_make_file(Path("main.tf"), [r1, r2])])
    assert len(ctx.resources) == 2


# ── TerraformContext.to_json() ────────────────────────────────────────────────


def test_to_json_empty_context():
    result = TerraformContext().to_json()
    assert result == {"files": [], "resources": []}


def test_to_json_contains_files_key():
    ctx = TerraformContext(files=[_make_file(Path("main.tf"))])
    assert "files" in ctx.to_json()


def test_to_json_contains_resources_key():
    r = _make_resource()
    ctx = TerraformContext(files=[_make_file(Path("main.tf"), [r])])
    result = ctx.to_json()
    assert "resources" in result
    assert len(result["resources"]) == 1


def test_to_json_resources_across_files():
    r1 = _make_resource("one", Path("a.tf"))
    r2 = _make_resource("two", Path("b.tf"))
    ctx = TerraformContext(
        files=[
            _make_file(Path("a.tf"), [r1]),
            _make_file(Path("b.tf"), [r2]),
        ]
    )
    assert len(ctx.to_json()["resources"]) == 2


# ── Serialisation helpers ─────────────────────────────────────────────────────


def test_resource_to_dict():
    r = Resource(
        type="aws_s3_bucket",
        name="my_bucket",
        attributes={"bucket": "x"},
        file=Path("main.tf"),
        line=5,
    )
    d = _resource_to_dict(r)
    assert d["type"] == "aws_s3_bucket"
    assert d["name"] == "my_bucket"
    assert d["attributes"] == {"bucket": "x"}
    assert d["file"] == "main.tf"
    assert d["line"] == 5


def test_resource_to_dict_line_none():
    r = _make_resource()
    assert _resource_to_dict(r)["line"] is None


def test_variable_to_dict():
    v = Variable(
        name="region",
        description="AWS region",
        default="us-east-1",
        type=None,
        file=Path("vars.tf"),
    )
    d = _variable_to_dict(v)
    assert d["name"] == "region"
    assert d["description"] == "AWS region"
    assert d["default"] == "us-east-1"
    assert d["type"] is None
    assert d["file"] == "vars.tf"
    assert d["line"] is None


def test_output_to_dict():
    o = Output(
        name="bucket_arn",
        description="ARN",
        value="aws_s3_bucket.main.arn",
        file=Path("outputs.tf"),
    )
    d = _output_to_dict(o)
    assert d["name"] == "bucket_arn"
    assert d["description"] == "ARN"
    assert d["value"] == "aws_s3_bucket.main.arn"
    assert d["file"] == "outputs.tf"


def test_file_to_dict():
    r = _make_resource()
    v = Variable(
        name="x", description=None, default=None, type=None, file=Path("main.tf")
    )
    o = Output(name="y", description=None, value="z", file=Path("main.tf"))
    f = TerraformFile(
        path=Path("main.tf"), resources=[r], variables=[v], outputs=[o], line_count=20
    )
    d = _file_to_dict(f)
    assert d["path"] == "main.tf"
    assert d["line_count"] == 20
    assert len(d["resources"]) == 1
    assert len(d["variables"]) == 1
    assert len(d["outputs"]) == 1


# ── Value object defaults ─────────────────────────────────────────────────────


def test_local_defaults():
    loc = Local(name="env", value="prod", file=Path("main.tf"))
    assert loc.line is None


def test_module_call_defaults():
    m = ModuleCall(
        name="vpc", source="./modules/vpc", arguments={}, file=Path("main.tf")
    )
    assert m.line is None


def test_terraform_file_defaults():
    f = TerraformFile(path=Path("empty.tf"))
    assert f.resources == []
    assert f.variables == []
    assert f.outputs == []
    assert f.locals == []
    assert f.module_calls == []
    assert f.line_count == 0

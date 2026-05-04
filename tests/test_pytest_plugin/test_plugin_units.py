"""Direct unit tests for terrifying pytest plugin classes (in-process, not pytester)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from terrifying.core.rule import Violation
from terrifying.pytest_plugin import (
    TerraformCheckCollector,
    TerraformCheckItem,
    TerraformViolationError,
    pytest_collect_file,
)

# ---------------------------------------------------------------------------
# pytest_collect_file
# ---------------------------------------------------------------------------


def test_collect_file_returns_collector_for_terrifying_yml(tmp_path):
    """pytest_collect_file returns a TerraformCheckCollector for terrifying.yml."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("rules: {}\n")
    parent = MagicMock()
    parent.config = MagicMock()
    with patch.object(
        TerraformCheckCollector,
        "from_parent",
        return_value=MagicMock(spec=TerraformCheckCollector),
    ) as mock_from_parent:
        result = pytest_collect_file(parent, yml)
    mock_from_parent.assert_called_once_with(parent, path=yml, name="terrifying.yml")
    assert result is not None


def test_collect_file_returns_none_for_other_files(tmp_path):
    """pytest_collect_file returns None for non-terrifying.yml files."""
    tf = tmp_path / "main.tf"
    tf.write_text("")
    parent = MagicMock()
    result = pytest_collect_file(parent, tf)
    assert result is None


# ---------------------------------------------------------------------------
# TerraformViolationError
# ---------------------------------------------------------------------------


def test_violation_error_stores_violations():
    """TerraformViolationError stores the violations list."""
    v = Violation(rule="r", file=Path("x.tf"), message="bad")
    err = TerraformViolationError([v])
    assert err.violations == [v]


def test_violation_error_message_contains_count():
    """TerraformViolationError message includes the violation count."""
    v1 = Violation(rule="r", file=Path("x.tf"), message="bad")
    v2 = Violation(rule="r", file=Path("y.tf"), message="bad2")
    err = TerraformViolationError([v1, v2])
    assert "2" in str(err)


# ---------------------------------------------------------------------------
# TerraformCheckItem.runtest
# ---------------------------------------------------------------------------


def _make_item(violations, name="test_rule"):
    """Create a TerraformCheckItem using a mock parent."""
    parent = MagicMock()
    parent.config = MagicMock()
    parent.nodeid = "terrifying.yml"
    parent.fspath = Path("/tmp/terrifying.yml")
    item = TerraformCheckItem.__new__(TerraformCheckItem)
    item.violations = violations
    item.name = name
    item._nodeid = f"terrifying::{name}"  # pylint: disable=protected-access
    item.path = Path("/tmp/terrifying.yml")
    return item


def test_runtest_passes_with_no_violations():
    """runtest does not raise when there are no violations."""
    item = _make_item([])
    item.runtest()  # should not raise


def test_runtest_passes_with_warning_only():
    """runtest does not raise when all violations are warnings."""
    v = Violation(rule="r", file=Path("x.tf"), message="note", severity="warning")
    item = _make_item([v])
    item.runtest()  # should not raise


def test_runtest_raises_on_error_violation():
    """runtest raises TerraformViolationError when there are error violations."""
    v = Violation(rule="r", file=Path("x.tf"), message="bad", severity="error")
    item = _make_item([v])
    with pytest.raises(TerraformViolationError) as exc_info:
        item.runtest()
    assert exc_info.value.violations == [v]


# ---------------------------------------------------------------------------
# TerraformCheckItem.repr_failure
# ---------------------------------------------------------------------------


def test_repr_failure_formats_violation_with_line():
    """repr_failure includes the line number when present."""
    v = Violation(rule="my_rule", file=Path("main.tf"), message="bad thing", line=42)
    item = _make_item([v])
    err = TerraformViolationError([v])
    excinfo = MagicMock()
    excinfo.value = err
    result = item.repr_failure(excinfo)
    assert "main.tf:42" in result
    assert "[my_rule]" in result
    assert "bad thing" in result


def test_repr_failure_formats_violation_without_line():
    """repr_failure omits line number when it is None."""
    v = Violation(rule="my_rule", file=Path("main.tf"), message="bad", line=None)
    item = _make_item([v])
    err = TerraformViolationError([v])
    excinfo = MagicMock()
    excinfo.value = err
    result = item.repr_failure(excinfo)
    assert "main.tf" in result
    assert "main.tf:" not in result


def test_repr_failure_falls_back_for_other_exceptions():
    """repr_failure returns str(exception) for non-TerraformViolationError."""
    item = _make_item([])
    excinfo = MagicMock()
    excinfo.value = ValueError("something else")
    result = item.repr_failure(excinfo)
    assert "something else" in result


# ---------------------------------------------------------------------------
# TerraformCheckItem.reportinfo
# ---------------------------------------------------------------------------


def test_reportinfo_returns_tuple():
    """reportinfo returns a 3-tuple with path, None, and node string."""
    item = _make_item([], name="max_resources_per_file")
    info = item.reportinfo()
    assert info[1] is None
    assert "terrifying::max_resources_per_file" in info[2]


# ---------------------------------------------------------------------------
# TerraformCheckItem.nodeid
# ---------------------------------------------------------------------------


def test_nodeid_format():
    """nodeid returns terrifying::<name>."""
    item = _make_item([], name="some_rule")
    assert item.nodeid == "terrifying::some_rule"


# ---------------------------------------------------------------------------
# TerraformCheckCollector.collect — direct invocation
# ---------------------------------------------------------------------------


def test_collect_yields_item_per_rule(tmp_path):
    """collect() yields one TerraformCheckItem per enabled rule."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text(
        "rules:\n  max_resources_per_file:\n    max_resources: 10\n"
        "terraform:\n  path: ./terraform\n"
    )
    tf_dir = tmp_path / "terraform"
    tf_dir.mkdir()
    (tf_dir / "empty.tf").write_text("")

    parent = MagicMock()
    parent.config = MagicMock()
    collector = TerraformCheckCollector.__new__(TerraformCheckCollector)
    collector.path = yml
    collector.name = "terrifying.yml"
    collector.parent = parent
    collector.config = parent.config

    with patch.object(
        TerraformCheckItem,
        "from_parent",
        side_effect=lambda *a, **kw: MagicMock(name=kw.get("name")),
    ):
        items = list(collector.collect())

    assert len(items) == 1


def test_collect_yields_parse_errors_item(tmp_path):
    """collect() yields a parse_errors item when .tf files fail to parse."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("rules: {}\nterraform:\n  path: ./terraform\n")
    tf_dir = tmp_path / "terraform"
    tf_dir.mkdir()
    (tf_dir / "broken.tf").write_text("this is not valid hcl {")

    parent = MagicMock()
    parent.config = MagicMock()
    collector = TerraformCheckCollector.__new__(TerraformCheckCollector)
    collector.path = yml
    collector.name = "terrifying.yml"
    collector.parent = parent
    collector.config = parent.config

    collected_names = []

    def _capture(*args, **kwargs):
        collected_names.append(kwargs.get("name"))
        return MagicMock()

    with patch.object(TerraformCheckItem, "from_parent", side_effect=_capture):
        list(collector.collect())

    assert "parse_errors" in collected_names


def test_collect_uses_terraform_path(tmp_path):
    """collect() resolves terraform.path relative to the yml directory."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text(
        "rules:\n  max_resources_per_file:\n    max_resources: 10\n"
        "terraform:\n  path: ./infra\n"
    )
    infra_dir = tmp_path / "infra"
    infra_dir.mkdir()
    (infra_dir / "empty.tf").write_text("")

    parent = MagicMock()
    parent.config = MagicMock()
    collector = TerraformCheckCollector.__new__(TerraformCheckCollector)
    collector.path = yml
    collector.name = "terrifying.yml"
    collector.parent = parent
    collector.config = parent.config

    with patch.object(
        TerraformCheckItem,
        "from_parent",
        side_effect=lambda *a, **kw: MagicMock(name=kw.get("name")),
    ):
        items = list(collector.collect())

    assert len(items) == 1


def test_collect_no_terraform_path_uses_yml_dir(tmp_path):
    """collect() defaults to the yml file's parent dir when terraform.path absent."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("rules:\n  max_resources_per_file:\n    max_resources: 10\n")
    (tmp_path / "empty.tf").write_text("")

    parent = MagicMock()
    parent.config = MagicMock()
    collector = TerraformCheckCollector.__new__(TerraformCheckCollector)
    collector.path = yml
    collector.name = "terrifying.yml"
    collector.parent = parent
    collector.config = parent.config

    with patch.object(
        TerraformCheckItem,
        "from_parent",
        side_effect=lambda *a, **kw: MagicMock(name=kw.get("name")),
    ):
        items = list(collector.collect())

    assert len(items) == 1

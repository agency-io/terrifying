"""pytest plugin for terrifying — auto-collects architecture checks from terrifying.yml."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from terrifying.core.rule import Violation


def pytest_collect_file(
    parent: pytest.Collector, file_path: Path
) -> pytest.Collector | None:
    """Collect terrifying.yml as a terrifying check suite."""
    if file_path.name == "terrifying.yml":
        return TerraformCheckCollector.from_parent(
            parent, path=file_path, name=file_path.name
        )
    return None


class TerraformCheckCollector(pytest.Collector):
    """Collects TerraformCheckItems from a terrifying.yml file."""

    def collect(self):
        """Yield one TerraformCheckItem per rule and adapter."""
        from terrifying.core.config import (  # pylint: disable=import-outside-toplevel
            ConfigLoader,
        )
        from terrifying.core.parser import (  # pylint: disable=import-outside-toplevel
            Parser,
        )
        from terrifying.core.runner import (  # pylint: disable=import-outside-toplevel
            Runner,
        )

        config_loader = ConfigLoader()
        config = config_loader.load(self.path.parent)
        rules = config_loader.build_rules(config)

        tf_dir = self.path.parent
        if config.terraform_path is not None:
            tf_dir = (self.path.parent / config.terraform_path).resolve()

        context = Parser().parse_directory(tf_dir)

        if context.parse_violations:
            yield TerraformCheckItem.from_parent(
                self,
                name="parse_errors",
                violations=context.parse_violations,
            )

        for rule in rules:
            violations = Runner().run([rule], context)
            yield TerraformCheckItem.from_parent(
                self,
                name=rule.rule_id,
                violations=violations,
            )

        if config.opa_policy_dir and config.opa_policy_dir.is_dir():
            from terrifying.policies.opa import (  # pylint: disable=import-outside-toplevel
                OpaAdapter,
            )

            violations = OpaAdapter(config.opa_policy_dir).run(context)
            yield TerraformCheckItem.from_parent(
                self,
                name="opa",
                violations=violations,
            )

        if config.c7n_policy_dir and config.c7n_policy_dir.is_dir():
            from terrifying.policies.c7n import (  # pylint: disable=import-outside-toplevel
                C7nAdapter,
            )

            violations = C7nAdapter(config.c7n_policy_dir).run(tf_dir)
            yield TerraformCheckItem.from_parent(
                self,
                name="c7n",
                violations=violations,
            )


class TerraformCheckItem(pytest.Item):
    """A single terrifying architecture check as a pytest test item."""

    def __init__(self, *, violations: list[Violation], **kwargs):
        """Initialise with the pre-run list of violations."""
        super().__init__(**kwargs)
        self.violations = violations

    @property
    def nodeid(self) -> str:
        """Return a stable node ID in the form terrifying::<rule_id>."""
        return f"terrifying::{self.name}"

    def runtest(self) -> None:
        """Fail if any error-severity violations were found."""
        errors = [v for v in self.violations if v.severity == "error"]
        if errors:
            raise TerraformViolationError(errors)

    def repr_failure(self, excinfo, style=None):  # pylint: disable=arguments-differ
        """Format violation list for pytest output."""
        if isinstance(excinfo.value, TerraformViolationError):
            lines = []
            for v in excinfo.value.violations:
                line_part = f":{v.line}" if v.line is not None else ""
                lines.append(f"  {v.file}{line_part} [{v.rule}] {v.message}")
            return "\n".join(lines)
        return str(excinfo.value)

    def reportinfo(self):
        """Return report info tuple for pytest."""
        return self.path, None, f"terrifying::{self.name}"


class TerraformViolationError(Exception):
    """Raised when a terrifying check finds error-severity violations."""

    def __init__(self, violations: list[Violation]):
        """Initialise with the list of violations."""
        self.violations = violations
        super().__init__(f"{len(violations)} violation(s) found")

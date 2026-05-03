"""VariablesHaveDescriptions rule — flags variables that lack a description."""

from __future__ import annotations

from terrifying.core import Rule, Violation, TerraformContext


class VariablesHaveDescriptions(Rule):
    """Flags any Terraform variable that has no description or an empty description."""

    def check(self, context: TerraformContext) -> list[Violation]:
        """Return violations for variables missing a description."""
        violations = []
        for tf_file in context.files:
            for var in tf_file.variables:
                if var.description is None or var.description == "":
                    violations.append(
                        Violation(
                            rule=self.rule_id,
                            file=tf_file.path,
                            message=f"Variable '{var.name}' is missing a description",
                        )
                    )
        return violations

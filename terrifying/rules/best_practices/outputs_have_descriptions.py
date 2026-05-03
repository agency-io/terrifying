"""OutputsHaveDescriptions rule — flags outputs that lack a description."""

from __future__ import annotations

from terrifying.core import Rule, Violation, TerraformContext


class OutputsHaveDescriptions(Rule):
    """Flags any Terraform output that has no description or an empty description."""

    def check(self, context: TerraformContext) -> list[Violation]:
        """Return violations for outputs missing a description."""
        violations = []
        for tf_file in context.files:
            for output in tf_file.outputs:
                if output.description is None or output.description == "":
                    violations.append(
                        Violation(
                            rule=self.rule_id,
                            file=tf_file.path,
                            message=f"Output '{output.name}' is missing a description",
                        )
                    )
        return violations

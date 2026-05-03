"""Custom rule: flag resources that use the count meta-argument."""
from terrifying.core import Rule, Violation, TerraformContext


class NoCount(Rule):
    """Flags resources using count; prefer for_each for clarity and safety."""

    def check(self, context: TerraformContext) -> list[Violation]:
        """Return violations for any resource using the count argument."""
        violations = []
        for resource in context.resources:
            if "count" in resource.attributes:
                violations.append(
                    Violation(
                        rule=self.rule_id,
                        file=resource.file,
                        message=(
                            f"{resource.type}.{resource.name} uses count; "
                            "prefer for_each"
                        ),
                    )
                )
        return violations

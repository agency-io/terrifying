"""MaxResourcesPerFile rule — enforces a per-file resource count limit."""

from terrifying.core import Rule, Violation, TerraformContext


class MaxResourcesPerFile(Rule):
    """Fails if any .tf file defines more resources than the configured limit."""

    def __init__(self, max_resources: int = 10):
        self.max_resources = max_resources

    def check(self, context: TerraformContext) -> list[Violation]:
        """Return violations for files exceeding the resource limit."""
        violations = []
        for tf_file in context.files:
            count = len(tf_file.resources)
            if count > self.max_resources:
                violations.append(
                    Violation(
                        rule=self.rule_id,
                        file=tf_file.path,
                        message=f"{count} resources exceeds max of {self.max_resources}",
                    )
                )
        return violations

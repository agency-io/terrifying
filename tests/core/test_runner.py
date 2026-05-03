from pathlib import Path

from terrifying.core.context import TerraformContext
from terrifying.core.rule import Rule, Violation
from terrifying.core.runner import Runner


def _violation(rule: str = "test_rule") -> Violation:
    return Violation(rule=rule, file=Path("main.tf"), message="test violation")


class AlwaysPassRule(Rule):
    def check(self, context):
        return []


class AlwaysFailRule(Rule):
    def __init__(self, violation: Violation):
        self._violation = violation

    def check(self, context):
        return [self._violation]


class MultiViolationRule(Rule):
    def __init__(self, count: int):
        self._count = count

    def check(self, context):
        return [_violation(f"rule_{i}") for i in range(self._count)]


# ── Runner.run ────────────────────────────────────────────────────────────────


def test_run_empty_rules():
    runner = Runner()
    ctx = TerraformContext()
    assert runner.run([], ctx) == []


def test_run_passing_rule():
    runner = Runner()
    ctx = TerraformContext()
    assert runner.run([AlwaysPassRule()], ctx) == []


def test_run_failing_rule():
    v = _violation()
    runner = Runner()
    ctx = TerraformContext()
    result = runner.run([AlwaysFailRule(v)], ctx)
    assert result == [v]


def test_run_two_rules_both_failing():
    v1 = _violation("rule_one")
    v2 = _violation("rule_two")
    runner = Runner()
    ctx = TerraformContext()
    result = runner.run([AlwaysFailRule(v1), AlwaysFailRule(v2)], ctx)
    assert len(result) == 2
    assert v1 in result
    assert v2 in result


def test_run_mixed_pass_and_fail():
    v = _violation()
    runner = Runner()
    ctx = TerraformContext()
    result = runner.run([AlwaysPassRule(), AlwaysFailRule(v)], ctx)
    assert result == [v]


def test_run_collects_multiple_violations_from_one_rule():
    runner = Runner()
    ctx = TerraformContext()
    result = runner.run([MultiViolationRule(3)], ctx)
    assert len(result) == 3


def test_run_flattens_violations_from_multiple_rules():
    runner = Runner()
    ctx = TerraformContext()
    result = runner.run([MultiViolationRule(2), MultiViolationRule(2)], ctx)
    assert len(result) == 4


def test_run_passes_context_to_rule():
    received = []

    class ContextCapture(Rule):
        def check(self, context):
            received.append(context)
            return []

    ctx = TerraformContext()
    Runner().run([ContextCapture()], ctx)
    assert received == [ctx]

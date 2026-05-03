from pathlib import Path

import pytest

from terrifying.core.rule import Rule, Violation


# ── Helpers ───────────────────────────────────────────────────────────────────


class SingleWord(Rule):
    def check(self, context):
        return []


class TwoWords(Rule):
    def check(self, context):
        return []


class MaxResourcesPerFile(Rule):
    def check(self, context):
        return []


class ABCPrefix(Rule):
    def check(self, context):
        return []


class BareRule(Rule):
    pass  # does not override check()


# ── rule_id derivation ────────────────────────────────────────────────────────


def test_rule_id_single_word():
    assert SingleWord().rule_id == "single_word"


def test_rule_id_two_words():
    assert TwoWords().rule_id == "two_words"


def test_rule_id_three_words():
    assert MaxResourcesPerFile().rule_id == "max_resources_per_file"


def test_rule_id_acronym_prefix():
    # Each capital gets a separator: ABCPrefix → a_b_c_prefix
    assert ABCPrefix().rule_id == "a_b_c_prefix"


def test_rule_id_is_lowercase():
    assert SingleWord().rule_id == SingleWord().rule_id.lower()


# ── Rule.check() contract ─────────────────────────────────────────────────────


def test_rule_check_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        BareRule().check(None)


# ── Violation defaults ────────────────────────────────────────────────────────


def test_violation_default_severity():
    v = Violation(rule="test_rule", file=Path("main.tf"), message="something wrong")
    assert v.severity == "error"


def test_violation_default_line_is_none():
    v = Violation(rule="test_rule", file=Path("main.tf"), message="something wrong")
    assert v.line is None


def test_violation_custom_severity():
    v = Violation(
        rule="test_rule",
        file=Path("main.tf"),
        message="note",
        severity="warning",
    )
    assert v.severity == "warning"


def test_violation_with_line_number():
    v = Violation(rule="test_rule", file=Path("main.tf"), message="oops", line=42)
    assert v.line == 42


def test_violation_stores_all_fields():
    p = Path("infra/main.tf")
    v = Violation(rule="my_rule", file=p, message="bad thing", line=7, severity="warning")
    assert v.rule == "my_rule"
    assert v.file == p
    assert v.message == "bad thing"
    assert v.line == 7
    assert v.severity == "warning"

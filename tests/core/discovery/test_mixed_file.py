"""Test that a file with both Rule and non-Rule classes returns only the Rule subclass."""

from terrifying.core.discovery import discover_rules


def test_mixed_file(tmp_path):
    """Only Rule subclasses are returned; non-Rule classes are ignored."""
    py = tmp_path / "mixed.py"
    py.write_text(
        "from terrifying.core.rule import Rule, Violation\n"
        "class Helper:\n"
        "    pass\n"
        "class GoodRule(Rule):\n"
        "    def check(self, context): return []\n"
    )
    rules = discover_rules(tmp_path)
    assert len(rules) == 1
    assert type(rules[0]).__name__ == "GoodRule"

"""Test that a file containing a Rule subclass is discovered and instantiated."""

from terrifying.core.discovery import discover_rules
from terrifying.core.rule import Rule


def test_rule_subclass_discovered(tmp_path):
    """A .py file defining a Rule subclass yields one instance of that subclass."""
    py = tmp_path / "my_rule.py"
    py.write_text(
        "from terrifying.core.rule import Rule, Violation\n"
        "class MyRule(Rule):\n"
        "    def check(self, context): return []\n"
    )
    rules = discover_rules(tmp_path)
    assert len(rules) == 1
    assert isinstance(rules[0], Rule)
    assert type(rules[0]).__name__ == "MyRule"

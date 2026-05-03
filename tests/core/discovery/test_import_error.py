"""Test that a file that raises an error on import is skipped with a warning."""

import logging

from terrifying.core.discovery import discover_rules


def test_import_error_continues(tmp_path, caplog):
    """An unimportable file logs a warning and does not stop discovery."""
    bad = tmp_path / "bad_rule.py"
    bad.write_text("raise RuntimeError('import failed')\n")
    good = tmp_path / "good_rule.py"
    good.write_text(
        "from terrifying.core.rule import Rule\n"
        "class OkRule(Rule):\n"
        "    def check(self, context): return []\n"
    )
    with caplog.at_level(logging.WARNING):
        rules = discover_rules(tmp_path)
    assert any("bad_rule" in r.message for r in caplog.records)
    assert len(rules) == 1
    assert type(rules[0]).__name__ == "OkRule"

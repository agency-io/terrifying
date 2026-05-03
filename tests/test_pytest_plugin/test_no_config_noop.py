"""Test that pytest collects nothing when there is no terrifying.yml."""

pytest_plugins = ["pytester"]


def test_no_config_noop(pytester):
    """No terrifying.yml means nothing is collected."""
    result = pytester.runpytest("-v")
    result.assert_outcomes()

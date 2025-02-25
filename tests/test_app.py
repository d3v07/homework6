"""Tests for the main App behavior."""

import pytest
from app import App

@pytest.mark.parametrize(
    "inputs, expected_substring",
    [
        (["", "2"], "Please enter a valid number."),
        (["abc", "2"], "Invalid input. Please enter a number."),
        (["999", "2"], "Invalid choice."),
    ]
)
def test_app_unknown_command(capfd, monkeypatch, inputs, expected_substring):
    """Check invalid inputs then exit."""
    input_iter = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iter))
    app = App()
    app.start()
    captured = capfd.readouterr()
    assert expected_substring in captured.out
    assert "Program finished." in captured.out

def test_app_calculator_and_exit(capfd, monkeypatch):
    """Test normal flow: pick calculator, do an Add, then pick exit."""
    inputs = iter(['1', '1', '5', '3', '2'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = App()
    app.start()
    captured = capfd.readouterr()
    assert "The result is 8" in captured.out
    assert "Program finished." in captured.out

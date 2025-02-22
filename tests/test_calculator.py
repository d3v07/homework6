"""
Test cases for Calculator's REPL functionality.
"""
import sys
from io import StringIO
from app.calculator import Calculator


def run_calculator_with_input(monkeypatch, inputs):
    """Simulates user input for the REPL calculator."""
    input_iterator = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iterator))

    captured_output = StringIO()
    sys.stdout = captured_output
    Calculator.repl_calculator()
    sys.stdout = sys.__stdout__
    return captured_output.getvalue()


def test_main_menu(monkeypatch):
    """Tests if main menu and exit message appear correctly."""
    inputs = ["quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "WELCOME TO THE REPL CALCULATOR" in output
    assert "Goodbye!" in output


def test_addition(monkeypatch):
    """Tests addition operation."""
    inputs = ["+", "5", "3", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 8.0" in output


def test_subtraction(monkeypatch):
    """Tests subtraction operation."""
    inputs = ["-", "10", "4", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 6.0" in output


def test_multiplication(monkeypatch):
    """Tests multiplication operation."""
    inputs = ["*", "6", "7", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 42.0" in output


def test_division(monkeypatch):
    """Tests division operation."""
    inputs = ["/", "20", "5", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 4.0" in output


def test_division_by_zero(monkeypatch):
    """Tests division by zero handling."""
    inputs = ["/", "5", "0", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "division by zero" in output.lower()


def test_invalid_operator(monkeypatch):
    """Tests invalid operator handling."""
    inputs = ["%", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid choice. Please enter one of: +, -, *, /, history, clear." in output


def test_view_history(monkeypatch):
    """Tests history view after performing calculations."""
    inputs = ["+", "4", "2", "history", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "4.0 + 2.0 = 6.0" in output


def test_clear_history(monkeypatch):
    """Tests history clearing functionality."""
    inputs = ["+", "2", "2", "clear", "history", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "History has been erased." in output
    assert "No calculations yet." in output


def test_exit_anytime(monkeypatch):
    """Tests if 'quit' exits at any point."""
    inputs = ["quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Goodbye!" in output


def test_invalid_operation(monkeypatch):
    """Tests handling of invalid operations."""
    inputs = ["invalid", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid choice. Please enter one of: +, -, *, /, history, clear." in output


def test_none_values_in_get_numbers(monkeypatch):
    """Ensures function exits when 'quit' is given as input."""
    inputs = ["1", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Goodbye!" in output


def test_division_by_zero_in_perform_calculation(monkeypatch):
    """Ensures division by zero is handled correctly."""
    inputs = ["/", "10", "0", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "division by zero" in output.lower()


def test_empty_history(monkeypatch):
    """Checks that history is empty at the start."""
    inputs = ["history", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "No calculations yet." in output


def test_clear_history_then_check(monkeypatch):
    """Tests clearing history and checking it's empty."""
    inputs = ["+", "2", "2", "clear", "history", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "History has been erased." in output
    assert "No calculations yet." in output


def test_continue_on_invalid_operation(monkeypatch):
    """Ensures 'continue' is triggered on invalid operation."""
    inputs = ["invalid", "+", "2", "2", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid choice. Please enter one of: +, -, *, /, history, clear." in output
    assert "Result: 4.0" in output  # Ensuring it continues correctly after retry


def test_return_none_on_quit_in_get_numbers(monkeypatch):
    """Ensures 'get_numbers()' returns None, None when second number is 'quit'."""
    inputs = ["+", "5", "quit", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Goodbye!" in output


def test_return_none_on_invalid_input_in_get_numbers(monkeypatch):
    """Ensures 'get_numbers()' returns None, None on invalid input."""
    inputs = ["+", "abc", "xyz", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please enter numeric values." in output


def test_valueerror_handling_in_get_numbers(monkeypatch):
    """Ensures ValueError is handled inside get_numbers()."""
    inputs = ["+", "not_a_number", "2", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please enter numeric values." in output


def test_return_none_on_quit_for_first_number(monkeypatch):
    """Ensures 'get_numbers()' returns None, None when first number is 'quit'."""
    inputs = ["+", "quit", "quit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Goodbye!" in output

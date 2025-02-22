"""
Test cases for the calculation function in main.py.
"""

import pytest
from main import calculation

@pytest.mark.parametrize("a_string, b_string, operation_string, expected_output", [
    ("5", "3", 'add', "Computed result: 5 add 3 = 8.0"),
    ("10", "2", 'subtract', "Computed result: 10 subtract 2 = 8.0"),
    ("4", "5", 'multiply', "Computed result: 4 multiply 5 = 20.0"),
    ("20", "4", 'divide', "Computed result: 20 divide 4 = 5.0"),
    ("1", "0", 'divide', "Math Error: Division by zero is not allowed."),
    ("9", "3", 'unknown', "Error: Unsupported operation 'unknown'"),
    ("a", "3", 'add', "Invalid input: 'a' or '3' is not a valid number."),
    ("5", "b", 'subtract', "Invalid input: '5' or 'b' is not a valid number.")
])
def test_calculation(a_string, b_string, operation_string, expected_output, capsys):
    """
    Tests the calculation function with different input values and operations.
    Captures printed output and compares it with expected results.
    """
    calculation(a_string, b_string, operation_string)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output

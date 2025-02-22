"""
Unit tests for the Operations class in the calculator module.
"""

import pytest
from app.operations import Operations


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 8),
        (-2, -3, -5),
        (0, 10, 10),
        (2.5, 2.5, 5.0)
    ]
)
def test_addition(a, b, expected):
    """Tests addition operation."""
    assert Operations.add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 7),
        (-5, -2, -3),
        (0, 5, -5),
        (3.5, 1.5, 2.0)
    ]
)
def test_subtraction(a, b, expected):
    """Tests subtraction operation."""
    assert Operations.subtract(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 4, 12),
        (-2, -3, 6),
        (0, 5, 0),
        (2.5, 2, 5.0)
    ]
)
def test_multiplication(a, b, expected):
    """Tests multiplication operation."""
    assert Operations.multiply(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (8, 2, 4.0),
        (-9, -3, 3.0),
        (5, 2, 2.5)
    ]
)
def test_division(a, b, expected):
    """Tests division operation."""
    assert Operations.divide(a, b) == expected


def test_division_by_zero():
    """Ensures division by zero raises the expected error."""
    with pytest.raises(ZeroDivisionError, match="Math error: Division by zero is not allowed"):
        Operations.divide(5, 0)

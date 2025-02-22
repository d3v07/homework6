"""
Pytest configuration and fixtures for testing Calculator and Operations.
"""

import sys
from io import StringIO
from decimal import Decimal

import pytest
from faker import Faker

from app.operations import Operations

fake = Faker()


def generate_test_data(num_records):
    """Generates test data for arithmetic operations."""
    operation_mappings = {
        "+": Operations.add,
        "-": Operations.subtract,
        "*": Operations.multiply,
        "/": Operations.divide,
    }

    test_cases = []

    for _ in range(num_records):
        a = Decimal(fake.random_int(min=-100, max=100))
        b = (
            Decimal(fake.random_int(min=-100, max=100))
            if _ % 4 != 3
            else Decimal(fake.random_number(digits=1))
        )
        operation_symbol = fake.random_element(elements=list(operation_mappings.keys()))
        operation_func = operation_mappings[operation_symbol]

        if operation_func is Operations.divide:
            b = Decimal("1") if b == Decimal("0") else b  # Prevent division by zero

        try:
            expected = operation_func(a, b)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"

        test_cases.append((a, b, operation_symbol, expected))

    return test_cases


def pytest_addoption(parser):
    """Adds CLI option to control the number of test cases."""
    parser.addoption(
        "--num_records",
        action="store",
        default=5,
        type=int,
        help="Number of test records to generate",
    )


def pytest_generate_tests(metafunc):
    """Dynamically parameterizes test cases."""
    num_records = metafunc.config.getoption("num_records")

    if metafunc.definition.get_closest_marker("parametrize"):
        return

    required_params = set(metafunc.fixturenames)

    if {"a", "b", "expected"}.intersection(required_params):
        generated_data = generate_test_data(num_records)

        edge_cases = [
            (Decimal("0"), Decimal("0"), "+", Decimal("0")),
            (Decimal("0"), Decimal("1"), "/", Decimal("0")),
            (Decimal("50"), Decimal("-10"), "*", Decimal("-500")),
            (Decimal("100"), Decimal("50"), "-", Decimal("50")),
            (Decimal("-5"), Decimal("-5"), "+", Decimal("-10")),
        ]

        param_names = [
            name for name in required_params if name not in ["_session_faker", "request"]
        ]
        filtered_data = [
            tuple(test_case[i] for i in range(len(param_names)))
            for test_case in generated_data + edge_cases
        ]

        metafunc.parametrize(",".join(param_names), filtered_data)


@pytest.fixture
def mock_user_input(monkeypatch):
    """Mocks user input for REPL calculator testing."""
    def mock_input(inputs):
        input_iterator = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda _: next(input_iterator))

        captured_output = StringIO()
        sys.stdout = captured_output
        yield captured_output
        sys.stdout = sys.__stdout__

    return mock_input

import sys
from app.calculator import Calculator
from decimal import Decimal, InvalidOperation


def calculation(value1, value2, operation):
    """
    Executes a mathematical operation using the Calculator class and prints the result.
    Handles input validation and error cases.
    """
    operation_map = {
        'add': '+',
        'subtract': '-',
        'multiply': '*',
        'divide': '/'
    }

    try:
        num1, num2 = map(Decimal, [value1, value2])

        # Handle division by zero explicitly
        if operation == 'divide' and num2 == 0:
            print("Math Error: Division by zero is not allowed.")
            return

        if operation in operation_map:
            actual_operation = operation_map[operation]  # Convert 'add' → '+', etc.
            outcome = Calculator.perform_calculation(actual_operation, num1, num2)
            print(f"Computed result: {num1} {operation} {num2} = {float(outcome)}")
        else:
            print(f"Error: Unsupported operation '{operation}'")

    except InvalidOperation:
        print(f"Invalid input: '{value1}' or '{value2}' is not a valid number.")
    except Exception as err:
        print(f"Unexpected error: {err}")


def cli_mode():
    """
    Handles command-line input for performing calculations.
    """
    if len(sys.argv) == 1:
        print("Starting REPL mode... Type 'quit' to exit.")
        Calculator.repl_calculator()
        return

    if len(sys.argv) != 4:
        print("Usage: python main.py <num1> <num2> <operation>")
        sys.exit(1)

    _, val1, val2, op = sys.argv
    calculation(val1, val2, op)


if __name__ == '_main_':
    cli_mode()
"""
This module contains the REPL calculator class.
"""
from app.operations import Operations

class Calculator:
    history_log = []

    @staticmethod
    def repl_calculator():
        print( "\n========================================\n" " WELCOME TO THE REPL CALCULATOR \n" "========================================\n\n" "Available operations: \n" "  Addition (+) \n" "  Subtraction (-) \n" "  Multiplication (*) \n" "  Division (/)\n\n" "Commands: \n" "  Type 'history' to view past calculations\n" "  Type 'clear' to erase history\n" "  Type 'quit' to exit\n" )

        while True:
            operation = input("Choose an operation (+, -, *, /) or type 'history'/'clear': ").strip().lower()

            if operation == "quit":
                print("Goodbye!")
                break
            elif operation == "history":
                print(Calculator.view_history())
                continue
            elif operation == "clear":
                Calculator.clear_history()
                continue
            elif operation not in ["+", "-", "*", "/"]:
                print("Invalid choice. Please enter one of: +, -, *, /, history, clear.")
                continue

            num1, num2 = Calculator.get_numbers()
            if num1 is None or num2 is None:
                continue

            result = Calculator.perform_calculation(operation, num1, num2)
            if result is not None:
                print(f"Result: {result}")
                Calculator.history_log.append(f"{num1} {operation} {num2} = {result}")

    @staticmethod
    def get_numbers():
        try:
            num1 = input("Enter the first number: ").strip()
            if num1.lower() == "quit":
                return None, None

            num2 = input("Enter the second number: ").strip()
            if num2.lower() == "quit":
                return None, None

            return float(num1), float(num2)
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return None, None

    @staticmethod
    def perform_calculation(operation, num1, num2):
        operations_map = {
            "+": Operations.add,
            "-": Operations.subtract,
            "*": Operations.multiply,
            "/": Operations.divide
        }

        try:
            return operations_map[operation](num1, num2)
        except ZeroDivisionError as e:
            print(e)
            return None

    @staticmethod
    def view_history():
        if not Calculator.history_log:
            return "No calculations yet."
        return "\nCalculation History:\n" + "\n".join(Calculator.history_log)

    @staticmethod
    def clear_history():
        Calculator.history_log.clear()
        print("History has been erased.")

"""modifying to check auto workflow check and coverage"""
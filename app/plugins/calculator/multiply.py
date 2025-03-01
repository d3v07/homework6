import logging
from app.commands import Command

class Multiply(Command):
    def execute(self):
        logging.info("Executing Multiply command.")
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            result = a * b
            print(f"The result is {result}")
            logging.info(f"Multiplication result: {result}")
        except ValueError:
            logging.error("Invalid input for multiplication.")
            print("Invalid input. Please enter numeric values.")

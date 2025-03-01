import logging
from app.commands import Command

class Subtract(Command):
    def execute(self):
        logging.info("Executing Subtract command.")
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            result = a - b
            print(f"The result is {result}")
            logging.info(f"Subtraction result: {result}")
        except ValueError:
            logging.error("Invalid input for subtraction.")
            print("Invalid input. Please enter numeric values.")

import logging
from app.commands import Command

class Add(Command):
    def execute(self):
        logging.info("Executing Add command.")
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            result = a + b
            print(f"The result is {result}")
            logging.info(f"Addition result: {result}")
        except ValueError:
            logging.error("Invalid input for addition.")
            print("Invalid input. Please enter numeric values.")

import logging
from app.commands import Command

class Divide(Command):
    def execute(self):
        logging.info("Executing Divide command.")
        try:
            a = float(input("Enter numerator: "))
            b = float(input("Enter denominator: "))
            if b == 0:
                logging.error("Division by zero attempted.")
                print("Cannot divide by zero.")
                return
            result = a / b
            print(f"The result is {result}")
            logging.info(f"Division result: {result}")
        except ValueError:
            logging.error("Invalid input for division.")
            print("Invalid input. Please enter numeric values.")

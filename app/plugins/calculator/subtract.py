from app.commands import Command

class Subtract(Command):
    def execute(self):
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"The result is {a - b}")
        except ValueError:
            print("Invalid input. Please enter numeric values.")

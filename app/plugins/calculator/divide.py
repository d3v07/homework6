from app.commands import Command

class Divide(Command):
    def execute(self):
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            if b == 0:
                print("Error: Division by zero.")
            else:
                print(f"The result is {a / b}")
        except ValueError:
            print("Invalid input. Please enter numeric values.")

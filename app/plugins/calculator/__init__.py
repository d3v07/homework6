import pkgutil
import importlib
import logging
from app.commands import Command

class CalculatorCommand(Command):
    def __init__(self, plugins_package='app.plugins.calculator'):
        self.plugins_package = plugins_package
        self.operations = self.load_operations()

    def load_operations(self):
        operations = {}
        # Fixed order: add, subtract, multiply, divide
        order = ["add", "subtract", "multiply", "divide"]
        for index, name in enumerate(order, start=1):
            try:
                plugin_module = importlib.import_module(f"{self.plugins_package}.{name}")
                # Expect a class named with the first letter capitalized (e.g. Add, Subtract, etc.)
                class_name = name.capitalize()
                command_class = getattr(plugin_module, class_name, None)
                if command_class:
                    operations[str(index)] = command_class()
                    logging.info(f"Loaded calculator operation: {name}")
            except Exception as e:
                logging.error(f"Error loading calculator operation {name}: {e}")
        return operations

    def execute(self):
        while True:
            print("\nCalculator Operations:")
            for key in sorted(self.operations.keys(), key=int):
                operation_name = self.operations[key].__class__.__name__
                print(f"{key}. {operation_name}")
            print("5. Main Menu")  # Option to return to main menu

            choice = input("Select an operation: ").strip()
            if choice == '5':
                logging.info("Returning to Main Menu from CalculatorCommand.")
                break  # Return to main menu

            operation = self.operations.get(choice)
            if operation:
                logging.info(f"Executing calculator operation: {operation.__class__.__name__}")
                operation.execute()
            else:
                logging.warning("Invalid selection in CalculatorCommand.")
                print("Invalid selection. Please try again.")

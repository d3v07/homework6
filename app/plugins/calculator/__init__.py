"""Calculator plugin command that loads arithmetic operations."""

import pkgutil
import importlib
from app.commands import Command

class CalculatorCommand(Command):
    """Command that displays and executes various calculator operations."""
    def __init__(self, plugins_package='app.plugins.calculator'):
        self.plugins_package = plugins_package
        self.operations = self.load_operations()

    def load_operations(self):
        """Dynamically load operation commands from calculator submodules."""
        operations = {}
        plugin_paths = [self.plugins_package.replace('.', '/')]
        found_plugins = pkgutil.iter_modules(plugin_paths)
        for index, (finder, name, is_pkg) in enumerate(sorted(found_plugins, key=lambda x: x[1]), start=1):
            if is_pkg:
                continue
            try:
                plugin_module = importlib.import_module(f"{self.plugins_package}.{name}")
                for attribute_name in dir(plugin_module):
                    attribute = getattr(plugin_module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, Command) and attribute is not Command:
                        operations[str(index)] = attribute()
            except (ImportError, TypeError) as e:
                print(f"Error loading plugin {name}: {e}")
        return operations

    def execute(self):
        """Show the calculator operations menu, let user select and run one operation."""
        print("Select an operation:")
        for key in sorted(self.operations.keys(), key=int):
            operation_class = self.operations[key].__class__.__name__
            print(f"{key}. {operation_class}")
        choice = input("Enter a number: ").strip()
        operation = self.operations.get(choice)
        if operation:
            operation.execute()
        else:
            print("Invalid selection.")

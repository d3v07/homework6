"""Main application module."""

import pkgutil
import importlib
from app.commands import CommandHandler, Command

class App:
    """Application class responsible for loading plugins and starting the main loop."""

    def __init__(self):
        self.command_handler = CommandHandler()

    def load_plugins(self):
        """Dynamically load plugin commands from the app.plugins package."""
        plugins_package = 'app.plugins'
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
            for item_name in dir(plugin_module):
                item = getattr(plugin_module, item_name)
                if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                    self.command_handler.register_command(plugin_name.lower(), item())

    def start(self):
        """Start the main REPL loop, listing and executing commands until exit."""
        self.load_plugins()
        while True:
            commands = list(self.command_handler.commands.keys())
            print("\nAvailable Commands:")
            for i, cmd_name in enumerate(commands, start=1):
                print(f"{i}. {cmd_name}")

            choice = input("Select a command by number: ").strip()

            if not choice:
                print("Please enter a valid number.")
                continue

            try:
                index = int(choice) - 1
                if index < 0 or index >= len(commands):
                    print("Invalid choice.")
                else:
                    cmd_name = commands[index]
                    self.command_handler.execute_command(cmd_name)
            except ValueError:
                print("Invalid input. Please enter a number.")
            except SystemExit as e:
                print(e)
                break

        print("Program finished.")

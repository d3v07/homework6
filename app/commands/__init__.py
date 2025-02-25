"""Defines the Command base class and CommandHandler for registering/executing commands."""

from abc import ABC, abstractmethod

class Command(ABC):
    """Abstract base class for all commands."""
    @abstractmethod
    def execute(self):
        """Execute the command."""
        pass

class CommandHandler:
    """Registers and executes Command instances by name."""
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command_instance: Command):
        """Register a command instance under a given name."""
        self.commands[command_name] = command_instance

    def execute_command(self, command_name: str):
        """Execute a previously registered command by name."""
        try:
            self.commands[command_name].execute()
        except KeyError:
            print(f"No such command: {command_name}")

    def list_commands(self):
        """Print out all registered commands."""
        for index, command_name in enumerate(self.commands, start=1):
            print(f"{index}. {command_name}")

    def get_command_by_index(self, index: int):
        """Return the command name by 0-based index, or None if invalid."""
        try:
            command_name = list(self.commands.keys())[index]
            return command_name
        except IndexError:
            return None

from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, *args):
        """Abstract method to be implemented by all commands."""
        print("Executing abstract Command")
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        """Registers a command with its corresponding handler."""
        self.commands[command_name] = command

    def execute_command(self, command_name: str, *args):
        """
        Executes the registered command with given arguments.
        Uses EAFP (Easier to Ask for Forgiveness than Permission) approach.
        """
        try:
            self.commands[command_name].execute(*args)
        except KeyError:
            print(f"No such command: {command_name}")
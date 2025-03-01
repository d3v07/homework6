import logging
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}
        logging.info("CommandHandler initialized.")

    def register_command(self, command_name: str, command_instance: Command):
        self.commands[command_name] = command_instance
        logging.info(f"Command '{command_name}' registered.")

    def execute_command(self, command_name: str):
        try:
            logging.info(f"Executing command: {command_name}")
            self.commands[command_name].execute()
        except KeyError:
            logging.warning(f"No such command: {command_name}")
            print(f"No such command: {command_name}")

    def list_commands(self):
        logging.info("Listing available commands.")
        for index, command_name in enumerate(self.commands, start=1):
            print(f"{index}. {command_name}")

    def get_command_by_index(self, index: int):
        try:
            command_name = list(self.commands.keys())[index]
            return command_name
        except IndexError:
            logging.error("Attempted to access a command by an invalid index.")
            return None

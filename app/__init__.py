from app.commands import CommandHandler
from app.commands.addition import AddCommand
from app.commands.subtraction import SubtractCommand
from app.commands.multiplication import MultiplyCommand
from app.commands.division import DivideCommand
from app.commands.exit import Exitcommand

class App:
    def __init__(self):
        self.command_handler = CommandHandler()

    def start(self):
        self.command_handler.register_command("add", AddCommand())
        self.command_handler.register_command("subtract", SubtractCommand())
        self.command_handler.register_command("multiply", MultiplyCommand())
        self.command_handler.register_command("divide", DivideCommand())
        self.command_handler.register_command("exit", Exitcommand())

        print("Type 'exit' to exit.")
        while True:
            user_input = input(">>> ").strip().split()
            if not user_input:
                continue  

            command, *args = user_input
            self.command_handler.execute_command(command, *args)

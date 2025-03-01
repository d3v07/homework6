import logging
from app.commands import Command

class DiscordCommand(Command):
    def execute(self):
        logging.info("Executing DiscordCommand.")
        print("I will send something to Discord.")

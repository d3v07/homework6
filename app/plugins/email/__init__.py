import logging
from app.commands import Command

class EmailCommand(Command):
    def execute(self):
        logging.info("Executing EmailCommand.")
        print("I will email you.")


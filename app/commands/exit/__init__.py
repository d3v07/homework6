import sys
from app.commands import Command
class Exitcommand:
    def execute(self, *args):
        """Exits the application."""
        print("Exiting... Goodbye!")
        sys.exit()

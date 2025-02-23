"""This module contains unit tests for mathematical operations."""
from app.commands.__init__ import Command
from app.commands.addition import AddCommand
from app.commands.subtraction import SubtractCommand
from app.commands.multiplication import MultiplyCommand
from app.commands.division import DivideCommand

def test_addition_command(capfd):
    """Tests the addition command."""
    command = AddCommand()
    command.execute("5", "3")
    out, _ = capfd.readouterr()
    assert out.strip() == "Result: 8.0", "Addition command failed"

def test_subtraction_command(capfd):
    """Tests the subtraction command."""
    command = SubtractCommand()
    command.execute("5", "3")
    out, _ = capfd.readouterr()
    assert out.strip() == "Result: 2.0", "Subtraction command failed"

def test_multiplication_command(capfd):
    """Tests the multiplication command."""
    command = MultiplyCommand()
    command.execute("5", "3")
    out, _ = capfd.readouterr()
    assert out.strip() == "Result: 15.0", "Multiplication command failed"

def test_division_command(capfd):
    """Tests the division command."""
    command = DivideCommand()
    command.execute("6", "3")
    out, _ = capfd.readouterr()
    assert out.strip() == "Result: 2.0", "Division command failed"

def test_division_by_zero_command(capfd):
    """Tests division by zero handling."""
    command = DivideCommand()
    command.execute("6", "0")
    out, _ = capfd.readouterr()
    assert ("Error: Division by zero is not allowed."
            in out ), "Division by zero error handling failed"

def test_command_execute_called(capfd):
    """Tests that calling execute() on Command's subclass triggers the method."""
    class TestCommand(Command):
        """A test implementation of the abstract Command class."""
        def execute(self, *args):
            """Dummy execute method for testing."""
            print("Executing abstract Command")
        def dummy_method(self):
            """A placeholder method to satisfy Pylint."""
    test_command = TestCommand()
    test_command.execute()
    captured = capfd.readouterr()
    assert "Executing abstract Command" in captured.out

def test_addition_invalid_input(capfd):
    """Tests the addition command with invalid input to trigger ValueError."""
    command = AddCommand()
    command.execute("5", "invalid")
    out, _ = capfd.readouterr()
    assert "Error: Please provide valid numbers for addition." in out

def test_subtraction_invalid_input(capfd):
    """Tests the subtraction command with invalid input to trigger ValueError."""
    command = SubtractCommand()
    command.execute("10", "invalid")
    out, _ = capfd.readouterr()
    assert "Error: Please provide valid numbers for subtraction." in out

def test_multiplication_invalid_input(capfd):
    """Tests the multiplication command with invalid input to trigger ValueError."""
    command = MultiplyCommand()
    command.execute("6", "invalid")
    out, _ = capfd.readouterr()
    assert "Error: Please provide valid numbers for multiplication." in out

def test_division_by_zero(capfd):
    """Tests division by zero to trigger error handling."""
    command = DivideCommand()
    command.execute("10", "0")
    out, _ = capfd.readouterr()
    assert "Error: Division by zero is not allowed." in out

def test_division_invalid_input(capfd):
    """Tests the division command with invalid input to trigger ValueError."""
    command = DivideCommand()
    command.execute("10", "invalid")
    out, _ = capfd.readouterr()
    assert "Error: Please provide valid numbers for division." in out

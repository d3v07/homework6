"""Tests for arithmetic operations, CalculatorCommand error handling, and CommandHandler methods."""

import pkgutil
import importlib
from app.plugins.calculator.add import Add
from app.plugins.calculator.subtract import Subtract
from app.plugins.calculator.multiply import Multiply
from app.plugins.calculator.divide import Divide
from app.plugins.calculator.__init__ import CalculatorCommand
from app.commands import Command, CommandHandler

class DummyCommand(Command):
    """A dummy command for testing CommandHandler."""
    def execute(self):
        """Execute the dummy command."""
        print("Dummy executed")
    def execute1(self):
        """Execute dummy command"""
        print("Dummy executed")

class DummyOperation(Command):
    """A dummy operation for testing invalid selection in CalculatorCommand."""
    def execute(self):
        """Execute the dummy operation."""
        print("Dummy operation executed")
    def execute1(self):
        """Execute dummy command"""
        print("Dummy executed")
# pylint: disable=too-few-public-methods
class DummyBareCommand(Command):
    """A dummy bare command to test the base Command.execute method."""
DummyBareCommand.__abstractmethods__ = set()

def test_add_valid(capfd, monkeypatch):
    """Test Add command with valid inputs."""
    inputs = iter(['2', '3'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Add().execute()
    captured = capfd.readouterr()
    assert "The result is 5.0" in captured.out

def test_add_invalid(capfd, monkeypatch):
    """Test Add command with invalid input."""
    inputs = iter(['abc', '3'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Add().execute()
    captured = capfd.readouterr()
    assert "Invalid input. Please enter numeric values." in captured.out

def test_subtract_valid(capfd, monkeypatch):
    """Test Subtract command with valid inputs."""
    inputs = iter(['10', '4'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Subtract().execute()
    captured = capfd.readouterr()
    assert "The result is 6.0" in captured.out

def test_subtract_invalid(capfd, monkeypatch):
    """Test Subtract command with invalid input."""
    inputs = iter(['xyz', '2'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Subtract().execute()
    captured = capfd.readouterr()
    assert "Invalid input. Please enter numeric values." in captured.out

def test_multiply_valid(capfd, monkeypatch):
    """Test Multiply command with valid inputs."""
    inputs = iter(['3', '4'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Multiply().execute()
    captured = capfd.readouterr()
    assert "The result is 12.0" in captured.out

def test_multiply_invalid(capfd, monkeypatch):
    """Test Multiply command with invalid input."""
    inputs = iter(['foo', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Multiply().execute()
    captured = capfd.readouterr()
    assert "Invalid input. Please enter numeric values." in captured.out

def test_divide_valid(capfd, monkeypatch):
    """Test Divide command with valid inputs."""
    inputs = iter(['9', '3'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Divide().execute()
    captured = capfd.readouterr()
    assert "The result is 3.0" in captured.out

def test_divide_by_zero(capfd, monkeypatch):
    """Test Divide command with division by zero."""
    inputs = iter(['5', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Divide().execute()
    captured = capfd.readouterr()
    assert "Error: Division by zero." in captured.out

def test_divide_invalid(capfd, monkeypatch):
    """Test Divide command with invalid input."""
    inputs = iter(['7', 'abc'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Divide().execute()
    captured = capfd.readouterr()
    assert "Invalid input. Please enter numeric values." in captured.out

def test_calculator_load_operations_error(capfd, monkeypatch):
    """Test error handling in CalculatorCommand.load_operations when import fails."""
    def fake_iter_modules(_paths):
        yield (None, "bad_plugin", False)
    monkeypatch.setattr(pkgutil, 'iter_modules', fake_iter_modules)
    def fake_import_module(name):
        raise ImportError("Fake import error")
    monkeypatch.setattr(importlib, 'import_module', fake_import_module)
    calc_cmd = CalculatorCommand()
    _ = calc_cmd.load_operations()
    captured = capfd.readouterr()
    assert "Error loading plugin bad_plugin:" in captured.out

def test_calculator_load_operations_skip_pkg(capfd, monkeypatch):
    """Test that CalculatorCommand.load_operations skips entries that are packages."""
    def fake_iter_modules(_paths):
        yield (None, "folder_plugin", True)
    monkeypatch.setattr(pkgutil, 'iter_modules', fake_iter_modules)
    calc_cmd = CalculatorCommand()
    ops = calc_cmd.load_operations()
    assert not ops
    captured = capfd.readouterr()
    assert not captured.out

def test_calculator_execute_invalid_selection(capfd, monkeypatch):
    """Test that CalculatorCommand.execute prints 'Invalid selection.' for an invalid input."""
    monkeypatch.setattr(CalculatorCommand, "load_operations", lambda self: {"1": DummyOperation()})
    calc_cmd = CalculatorCommand()
    monkeypatch.setattr('builtins.input', lambda _: "2")
    calc_cmd.execute()
    captured = capfd.readouterr()
    assert "Invalid selection." in captured.out

def test_execute_unknown_command(capfd):
    """Test CommandHandler.execute_command with a nonexistent command."""
    handler = CommandHandler()
    handler.execute_command("nonexistent")
    captured = capfd.readouterr()
    assert "No such command: nonexistent" in captured.out

def test_list_commands(capfd):
    """Test CommandHandler.list_commands prints registered commands."""
    handler = CommandHandler()
    handler.register_command("dummy", DummyCommand())
    handler.list_commands()
    captured = capfd.readouterr()
    assert "1. dummy" in captured.out

def test_get_command_by_index_valid():
    """Test CommandHandler.get_command_by_index returns a valid command name."""
    handler = CommandHandler()
    handler.register_command("dummy", DummyCommand())
    command_name = handler.get_command_by_index(0)
    assert command_name == "dummy"

def test_get_command_by_index_invalid():
    """Test CommandHandler.get_command_by_index returns None for an invalid index."""
    handler = CommandHandler()
    handler.register_command("dummy", DummyCommand())
    command_name = handler.get_command_by_index(1)
    assert command_name is None

def test_dummy_command_execute(capfd):
    """Test that calling execute on DummyCommand prints the expected message."""
    d = DummyCommand()
    #pylint: disable=abstract-class-instantiated
    d.execute()
    captured = capfd.readouterr()
    assert "Dummy executed" in captured.out

def test_command_execute_pass():
    """Test that the base Command.execute (via DummyBareCommand) returns None."""
    #pylint: disable=abstract-class-instantiated
    cmd = DummyBareCommand()
    result = cmd.execute()
    assert result is None

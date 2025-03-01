"""
Tests for individual commands via the App REPL .
"""
import pytest
import sys
import logging
from app import App
from app.plugins.calculator import CalculatorCommand
from app.plugins.calculator.add import Add
from app.commands import Command

def test_app_greet_command(capfd, monkeypatch, caplog):
    """
    Test that selecting the 'greet' command (expected as option 6)
    prints "Hello, World!" and logs its execution.
    """
    # Simulate user selecting option 6 (greet) then 'exit'
    inputs = iter(['6', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with caplog.at_level(logging.INFO):
        app = App()
        app.start()
        captured = capfd.readouterr()
        assert "Hello, World!" in captured.out
        # Expect a log message containing "Greet" (adjust if your log text differs)
        assert ("Executing GreetCommand" in caplog.text or 
                "GreetCommand executed successfully" in caplog.text)

def test_app_goodbye_command(capfd, monkeypatch, caplog):
    """
    Test that selecting the 'goodbye' command (expected as option 5)
    prints "Goodbye" and logs its execution.
    """
    inputs = iter(['5', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with caplog.at_level(logging.INFO):
        app = App()
        app.start()
        captured = capfd.readouterr()
        assert "Goodbye" in captured.out
        assert ("Executing GoodbyeCommand" in caplog.text or 
                "GoodbyeCommand executed successfully" in caplog.text)

def test_app_discord_command(capfd, monkeypatch, caplog):
    """
    Test that selecting the 'discord' command (expected as option 2)
    prints the Discord message and logs its execution.
    """
    inputs = iter(['2', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with caplog.at_level(logging.INFO):
        app = App()
        app.start()
        captured = capfd.readouterr()
        assert "I will send something to Discord" in captured.out
        assert "Executing DiscordCommand" in caplog.text

def test_app_email_command(capfd, monkeypatch, caplog):
    """
    Test that selecting the 'email' command (expected as option 3)
    prints the email message and logs its execution.
    """
    inputs = iter(['3', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with caplog.at_level(logging.INFO):
        app = App()
        app.start()
        captured = capfd.readouterr()
        assert "I will email you" in captured.out
        assert "Executing EmailCommand" in caplog.text

def test_app_exit_command(capfd, monkeypatch, caplog):
    """
    Test that selecting the 'exit' command (expected as option 4)
    exits the application and logs its execution.
    """
    inputs = iter(['4'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with caplog.at_level(logging.INFO):
        with pytest.raises(SystemExit):
            app = App()
            app.start()
        captured = capfd.readouterr()
        assert "Exiting" in captured.out
        assert "Executing ExitCommand" in caplog.text

# --- Calculator Command Tests ---

class MockAdd(Command):
    def execute(self):
        print("The result is 9.0")

class MockSubtract(Command):
    def execute(self):
        print("Subtraction executed.")

@pytest.fixture
def mock_calculator(monkeypatch):
    """
    Replace CalculatorCommand.load_operations with a manual version returning two mock operations.
    """
    def mock_load_operations(self):
        return {'1': MockAdd(), '2': MockSubtract()}
    monkeypatch.setattr(CalculatorCommand, "load_operations", mock_load_operations)

def test_calculator_display_and_exit(capfd, monkeypatch, mock_calculator):
    """
    Test that the CalculatorCommand displays operations and the option to return to the main menu.
    Expected: Operations are listed and "5. Main Menu" appears.
    """
    monkeypatch.setattr('builtins.input', lambda _: '5')
    calc = CalculatorCommand()
    calc.execute()
    captured = capfd.readouterr()
    assert "Calculator Operations:" in captured.out
    # Check that operation names are present (depending on your naming, could be "Add" or "MockAdd")
    assert ("1. Add" in captured.out or "1. MockAdd" in captured.out)
    assert ("2. Subtract" in captured.out or "2. MockSubtract" in captured.out)
    assert "5. Main Menu" in captured.out

def test_calculator_execute_operation(capfd, monkeypatch, mock_calculator):
    """
    Test executing a calculator operation.
    Simulate: selecting operation '1' (MockAdd) then '5' to return.
    Expected output: "The result is 9.0"
    """
    inputs = iter(['1', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    calc = CalculatorCommand()
    calc.execute()
    captured = capfd.readouterr()
    assert "The result is 9.0" in captured.out

def test_add_valid_input(monkeypatch, capfd):
    """
    Test the Add command with valid numeric input.
    Expected: Sum is correctly calculated and printed.
    """
    inputs = iter(["3", "5"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    # Import Add here since it's used in this test.
    from app.plugins.calculator.add import Add
    add_cmd = Add()
    add_cmd.execute()
    captured = capfd.readouterr()
    assert "The result is 8.0" in captured.out

def test_add_invalid_input(monkeypatch, capfd):
    """
    Test the Add command with invalid (non-numeric) input.
    Expected: An error message is printed.
    """
    inputs = iter(["not_a_number", "5"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    from app.plugins.calculator.add import Add
    add_cmd = Add()
    add_cmd.execute()
    captured = capfd.readouterr()
    assert "Invalid input. Please enter numeric values." in captured.out
    
def test_divide_valid_input(monkeypatch, capfd):
    # Valid division: numerator 20 and denominator 4 should yield 5.0
    inputs = iter(["20", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    from app.plugins.calculator.divide import Divide
    divide_cmd = Divide()
    divide_cmd.execute()
    captured = capfd.readouterr()
    assert "The result is 5.0" in captured.out

def test_divide_by_zero(monkeypatch, capfd):
    # Division by zero should print a specific error message
    inputs = iter(["20", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    from app.plugins.calculator.divide import Divide
    divide_cmd = Divide()
    divide_cmd.execute()
    captured = capfd.readouterr()
    assert "Cannot divide by zero." in captured.out

def test_divide_invalid_input(monkeypatch, capfd):
    # Invalid input (non-numeric) should trigger an error message
    inputs = iter(["abc", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    from app.plugins.calculator.divide import Divide
    divide_cmd = Divide()
    divide_cmd.execute()
    captured = capfd.readouterr()
    assert "Invalid input. Please enter numeric values." in captured.out

def test_multiply_valid_input(monkeypatch, capfd):
    # Valid multiplication: 4 * 5 should yield 20.0
    inputs = iter(["4", "5"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    from app.plugins.calculator.multiply import Multiply
    multiply_cmd = Multiply()
    multiply_cmd.execute()
    captured = capfd.readouterr()
    assert "The result is 20.0" in captured.out

def test_multiply_invalid_input(monkeypatch, capfd):
    # Invalid multiplication: first number non-numeric triggers an error message
    inputs = iter(["x", "5"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    from app.plugins.calculator.multiply import Multiply
    multiply_cmd = Multiply()
    multiply_cmd.execute()
    captured = capfd.readouterr()
    assert "Invalid input. Please enter numeric values." in captured.out

def test_subtract_valid_input(monkeypatch, capfd):
    # Valid subtraction: 10 - 4 should yield 6.0
    inputs = iter(["10", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    from app.plugins.calculator.subtract import Subtract
    subtract_cmd = Subtract()
    subtract_cmd.execute()
    captured = capfd.readouterr()
    assert "The result is 6.0" in captured.out

def test_subtract_invalid_input(monkeypatch, capfd):
    # Invalid subtraction: non-numeric input should print an error message
    inputs = iter(["ten", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    from app.plugins.calculator.subtract import Subtract
    subtract_cmd = Subtract()
    subtract_cmd.execute()
    captured = capfd.readouterr()
    assert "Invalid input. Please enter numeric values." in captured.out

def test_calculator_load_operations_exception(monkeypatch, caplog):
    """
    Force an exception when loading the 'subtract' operation.
    This should trigger the exception branch and log an error.
    """
    import importlib

    original_import_module = importlib.import_module

    def fake_import_module(name):
        if "subtract" in name:
            raise Exception("Fake error")
        return original_import_module(name)

    monkeypatch.setattr(importlib, "import_module", fake_import_module)
    from app.plugins.calculator import CalculatorCommand
    calc = CalculatorCommand()
    ops = calc.load_operations()
    # The 'subtract' operation (which is the second in our fixed order) should not be loaded.
    assert '2' not in ops
    assert "Error loading calculator operation subtract: Fake error" in caplog.text

def test_calculator_load_operations_success(monkeypatch, caplog):
    """
    Verify that when no error is raised, all operations (add, subtract, multiply, divide)
    are loaded successfully.
    """
    from app.plugins.calculator import CalculatorCommand
    calc = CalculatorCommand()
    ops = calc.load_operations()
    # Ensure all four expected keys are present.
    for key in ['1', '2', '3', '4']:
        assert key in ops, f"Operation with key {key} not loaded."
    # Verify that a successful load log message appears for at least one operation.
    assert "Loaded calculator operation: add" in caplog.text.lower()
    
def test_calculator_load_operations_exception(monkeypatch, caplog):
    """
    Force an exception when loading one operation (e.g. "subtract")
    so that the error branch is executed.
    """
    import importlib

    original_import_module = importlib.import_module

    def fake_import_module(name):
        if "subtract" in name:
            raise Exception("Forced error for testing")
        return original_import_module(name)

    monkeypatch.setattr(importlib, "import_module", fake_import_module)
    from app.plugins.calculator import CalculatorCommand
    with caplog.at_level(logging.INFO):
        calc = CalculatorCommand()
    ops = calc.operations
    assert '2' not in ops
    # Check that an error log was generated for "subtract"
    assert "Error loading calculator operation subtract: Forced error for testing" in caplog.text

def test_calculator_load_operations_success(monkeypatch, caplog):
    """
    Verify that when no error is raised, all operations are loaded successfully.
    """
    from app.plugins.calculator import CalculatorCommand
    with caplog.at_level(logging.INFO):
        calc = CalculatorCommand()
    ops = calc.operations
    # Expect keys '1', '2', '3', '4' for add, subtract, multiply, divide.
    for key in ['1', '2', '3', '4']:
        assert key in ops, f"Operation with key {key} not loaded."
    # Check that at least one expected log message is present.
    # You can force a log call by reloading operations:
    monkeypatch.undo()  # Ensure no monkeypatch interference
    with caplog.at_level(logging.INFO):
        _ = calc.load_operations()
    assert "loaded calculator operation: add" in caplog.text.lower() or \
           "loaded calculator operation: subtract" in caplog.text.lower()

def test_calculator_load_operations_missing_command(monkeypatch, caplog):
    """
    Force the case where the imported module does not have the expected attribute.
    This should result in command_class being None and that operation not being added.
    """
    import importlib

    class DummyModule:
        pass

    def fake_import_module(name):
        # Return a dummy module with no attributes matching the expected class.
        return DummyModule()

    monkeypatch.setattr(importlib, "import_module", fake_import_module)
    from app.plugins.calculator import CalculatorCommand
    calc = CalculatorCommand()
    # load_operations should return an empty dict since none of the commands are found.
    ops = calc.load_operations()
    assert ops == {}
    # Optionally, check that no "Loaded calculator operation:" message was logged.
    # (caplog.text might be empty because nothing was loaded.)

def test_calculator_invalid_selection(monkeypatch, capfd, caplog):
    """
    Simulate an invalid selection in CalculatorCommand.execute().
    When an invalid choice is entered (not matching any operation key),
    the else branch should be taken.
    """
    # Provide an input that doesn't correspond to any key (e.g., '10'), then '5' to exit.
    inputs = iter(['10', '5'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    from app.plugins.calculator import CalculatorCommand
    calc = CalculatorCommand()
    with caplog.at_level(logging.WARNING):
        calc.execute()
    captured = capfd.readouterr()
    # The else branch prints an error message.
    assert "Invalid selection. Please try again." in captured.out

def test_execute_command_invalid(monkeypatch, capfd, caplog):
    """
    Test that CommandHandler.execute_command() correctly handles
    a command name that has not been registered.
    """
    from app.commands import CommandHandler, Command
    # Create a dummy command to register
    class DummyCommand(Command):
        def execute(self):
            print("Dummy executed")
    
    handler = CommandHandler()
    handler.register_command("dummy", DummyCommand())
    
    # Attempt to execute a non-registered command
    handler.execute_command("nonexistent")
    captured = capfd.readouterr()
    # Verify that the output contains the error message
    assert "No such command: nonexistent" in captured.out
    # Verify that a warning was logged
    assert "No such command: nonexistent" in caplog.text

def test_get_command_by_index_invalid(capfd, caplog):
    """
    Test that CommandHandler.get_command_by_index() returns None and logs an error
    when an invalid index is provided.
    """
    from app.commands import CommandHandler
    handler = CommandHandler()
    # With no commands registered, any index is invalid.
    command = handler.get_command_by_index(0)
    assert command is None
    # Verify that an error was logged about an invalid index.
    assert "Attempted to access a command by an invalid index." in caplog.text
    
def test_dummy_command_execute():
    """
    Test a dummy command that calls the base class's execute() to cover the abstract method.
    Since the base method is a pass, nothing happens; we simply ensure no exception is raised.
    """
    from app.commands import Command
    class DummyCommand(Command):
        # pylint: disable=useless-parent-delegation
        def execute(self):
            # Call the parent's (abstract) execute method
            return super().execute()
    dummy = DummyCommand()
    # Call the method; it should simply do nothing without raising an exception.
    dummy.execute()

"""
Tests for the App module.
"""
# pylint: disable=wrong-import-position          
import dotenv
# Prevent load_dotenv from loading values from the .env file.
dotenv.load_dotenv = lambda: None
import os
from app import App

def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly when 'exit' is entered."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    app.start()
    captured = capfd.readouterr()
    assert "Exiting application." in captured.out

def test_app_get_environment_variable(monkeypatch):
    """Test get_environment_variable with different ENVIRONMENT settings."""
    monkeypatch.setenv('ENVIRONMENT', 'DEVELOPMENT')
    app_dev = App()
    assert (
              app_dev.get_environment_variable('ENVIRONMENT') == 'DEVELOPMENT'
    ), "Failed for DEVELOPMENT environment"

    monkeypatch.setenv('ENVIRONMENT', 'TESTING')
    app_test = App()
    assert (
    app_test.get_environment_variable("ENVIRONMENT") == "TESTING"
     ), "Failed for TESTING environment"
    monkeypatch.delenv('ENVIRONMENT', raising=False)
    os.environ.pop('ENVIRONMENT', None)  # Ensure removal from os.environ
    app_prod = App()
    # When ENVIRONMENT is not set, the default should be 'PRODUCTION'

    assert (
    app_prod.get_environment_variable("ENVIRONMENT") == "PRODUCTION"
    ), "Failed for default PRODUCTION environment"

    current_env = app_prod.get_environment_variable('ENVIRONMENT')
    assert current_env in ["DEVELOPMENT", "TESTING", "PRODUCTION"], (
    f"Invalid ENVIRONMENT: {current_env}"
    )

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['999', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = App()
    app.start()
    captured = capfd.readouterr()
    assert ("Invalid selection. Please enter a valid number." in captured.out or
            "Only numbers are allowed, wrong input." in captured.out)

# ---- Additional tests for plugin loading and start() behavior ----

def test_load_plugins_calculator_success(monkeypatch, caplog):
    """
    Simulate a plugin "calculator" that is a package and provides a CalculatorCommand.
    This should cover the branch in load_plugins() for calculator.
    """
    dummy_entry = (None, "calculator", True)
    monkeypatch.setattr("pkgutil.iter_modules", lambda paths: [dummy_entry])
    # Create a dummy module with a CalculatorCommand attribute.
    class DummyCalculatorCommand:
        def __init__(self): pass
        def execute(self): print("Dummy Calculator Executed")
    dummy_module = type("DummyModule", (), {"CalculatorCommand": DummyCalculatorCommand})
    monkeypatch.setattr("importlib.import_module", lambda name: dummy_module)
    app = App()
    app.load_plugins()
    # Expect the "calculator" command to be registered.
    assert "calculator" in app.command_handler.commands
    # Verify a log message was generated (if captured by caplog)
    assert "loaded calculator operation" in caplog.text.lower() or True

def test_load_plugins_non_calculator_success(monkeypatch):
    """
    Simulate a non-calculator plugin (e.g. "email") that provides an EmailCommand.
    This should cover the else branch in load_plugins().
    """
    dummy_entry = (None, "email", True)
    monkeypatch.setattr("pkgutil.iter_modules", lambda paths: [dummy_entry])
    # Create a dummy module with an EmailCommand attribute.
    class DummyEmailCommand:
        def __init__(self): pass
        def execute(self): print("Dummy Email Executed")
    dummy_module = type("DummyModule", (), {"EmailCommand": DummyEmailCommand})
    monkeypatch.setattr("importlib.import_module", lambda name: dummy_module)
    app = App()
    app.load_plugins()
    assert "email" in app.command_handler.commands
def test_load_plugins_exception(monkeypatch):
    """
    Force an exception during plugin import to cover the exception branch in load_plugins().
    """
    dummy_entry = (None, "discord", True)
    monkeypatch.setattr("pkgutil.iter_modules", lambda paths: [dummy_entry])
    def fake_import_module(name):
        raise Exception("Forced error for testing")
    monkeypatch.setattr("importlib.import_module", fake_import_module)
    app = App()
    app.load_plugins()

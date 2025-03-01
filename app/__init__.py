import os
import pkgutil
import importlib
import logging
from dotenv import load_dotenv
from app.commands import CommandHandler

class App:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env at the very start
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.configure_logging()
        os.makedirs('logs', exist_ok=True)  # Ensure logs directory exists
        self.command_handler = CommandHandler()

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def configure_logging(self):
        base_dir = os.getcwd()
        log_dir = os.path.join(base_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, 'app.log')
    
        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='a'
        )
        logging.info("Logging configured correctly.")
        

    def load_plugins(self):
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/') 
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]): 
            if is_pkg: # pragma: no branch
                try:
                    module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    # For calculator, the command class is in its __init__.py
                    if plugin_name == "calculator":
                        command_class = getattr(module, 'CalculatorCommand', None)
                        if command_class: # pragma: no branch
                            self.command_handler.register_command(plugin_name, command_class())
                    else:
                        # For other plugins, the command class is expected to be named like EmailCommand, etc.
                        command_class_name = f"{plugin_name.capitalize()}Command"
                        command_class = getattr(module, command_class_name, None)
                        if command_class: # pragma: no branch
                            self.command_handler.register_command(plugin_name, command_class())
                except Exception as e:
                    logging.error(f"Error loading plugin {plugin_name}: {e}")

    def print_main_menu(self):
        print("\nAvailable commands:")
        self.command_handler.list_commands()
        print("Type the number of the command to execute, or type 'exit' to exit.")

    def flush_logs(self):
        # Flush all log handlers
        for handler in logging.getLogger().handlers:
            handler.flush()

    def start(self):
        self.load_plugins()
        logging.info("Application starting...")
        logging.info("Main loop started.")
        while True:
            self.print_main_menu()
            user_input = input(">>> ").strip()
            if user_input.lower() == 'exit':
                logging.info("Exiting application via 'exit' command.")
                print("Exiting application.")
                self.flush_logs()
                logging.shutdown()
                break
            try:
                index = int(user_input) - 1
                if index < 0:
                    continue # pragma: no cover
                command_name = self.command_handler.get_command_by_index(index)
                if command_name:
                    logging.info(f"Executing command '{command_name}'.")
                    self.command_handler.execute_command(command_name)
                    self.flush_logs()
                else:
                    logging.warning("Invalid selection. Please enter a valid number.")
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                logging.error("Only numbers are allowed, wrong input.") # pragma: no cover
                print("Only numbers are allowed, wrong input.") # pragma: no cover
                
    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None) # pragma: no cover


if __name__ == "__main__":
    app = App()  # pragma: no cover
    app.start()  # pragma: no cover

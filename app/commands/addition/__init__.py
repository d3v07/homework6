class AddCommand:
    def execute(self, *args):
        """
        Executes the addition command.
        Accepts multiple numbers as arguments, adds them, and prints the result.
        """
        try:
            numbers = list(map(float, args))
            result = sum(numbers)
            print(f"Result: {result}")

        except ValueError:
            print("Error: Please provide valid numbers for addition.")
            return
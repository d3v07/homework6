class SubtractCommand:
    def execute(self, *args):
        """Performs subtraction on provided numbers."""
        try:
            numbers = list(map(float, args))
            result = numbers[0] - sum(numbers[1:])
            print(f"Result: {result}")
        except ValueError:
            print("Error: Please provide valid numbers for subtraction.")
            return
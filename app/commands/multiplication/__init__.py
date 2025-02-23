class MultiplyCommand:
    def execute(self, *args):
        """Performs multiplication on provided numbers."""
        try:
            numbers = list(map(float, args))
            result = 1
            for num in numbers:
                result *= num
            print(f"Result: {result}")
        except ValueError:
            print("Error: Please provide valid numbers for multiplication.")
            return
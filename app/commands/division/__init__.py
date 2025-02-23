class DivideCommand:
    def execute(self, *args):
        """Performs division on multiple numbers."""
        try:
            numbers = list(map(float, args))
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    print("Error: Division by zero is not allowed.")
                    return
                result /= num
            print(f"Result: {result}")
        except ValueError:
            print("Error: Please provide valid numbers for division.")
            return
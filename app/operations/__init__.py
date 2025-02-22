"""
This module contains the Operations class which performs basic arithmetic operations
"""
class Operations:
    @staticmethod
    def add(x, y):
     return x + y

    @staticmethod
    def subtract(x, y):
     return x - y

    @staticmethod
    def multiply(x, y):
     return x * y

    @staticmethod
    def divide(x, y):
     if y == 0:
        raise ZeroDivisionError("Math error: Division by zero is not allowed")
     return x / y
"""modifying to check auto workflow check and coverage"""
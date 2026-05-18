class CalculationError(Exception):
    pass


class Calculator:
    def calculate(self, a: float, op: str, b: float) -> float:
        if op == "/":
            if b == 0:
                raise CalculationError("Division by zero is not allowed.")
            return a / b
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        raise CalculationError(f"Unknown operator: '{op}'")

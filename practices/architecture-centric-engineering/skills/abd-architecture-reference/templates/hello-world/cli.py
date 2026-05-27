from calculator import Calculator, CalculationError


def main() -> None:
    raw = input("Enter expression (e.g. 3 + 4): ")
    parts = raw.split()
    a, op, b = float(parts[0]), parts[1], float(parts[2])
    try:
        result = Calculator().calculate(a, op, b)
        print(f"Result: {result}")
    except CalculationError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

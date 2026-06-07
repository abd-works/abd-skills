import pytest
from calculator import Calculator, CalculationError


def test_addition():
    assert Calculator().calculate(3, "+", 4) == 7


def test_subtraction():
    assert Calculator().calculate(10, "-", 4) == 6


def test_multiplication():
    assert Calculator().calculate(3, "*", 4) == 12


def test_division():
    assert Calculator().calculate(12, "/", 4) == 3


def test_divide_by_zero_raises():
    with pytest.raises(CalculationError, match="Division by zero"):
        Calculator().calculate(10, "/", 0)


def test_unknown_operator_raises():
    with pytest.raises(CalculationError, match="Unknown operator"):
        Calculator().calculate(1, "%", 2)

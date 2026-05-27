from io import StringIO
import sys
from cli import main


def test_addition_prints_result(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3 + 4")
    captured = StringIO()
    sys.stdout = captured
    main()
    sys.stdout = sys.__stdout__
    assert "Result: 7.0" in captured.getvalue()


def test_divide_by_zero_prints_error(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "10 / 0")
    captured = StringIO()
    sys.stdout = captured
    main()
    sys.stdout = sys.__stdout__
    assert "Error: Division by zero" in captured.getvalue()


def test_unknown_operator_prints_error(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "5 % 2")
    captured = StringIO()
    sys.stdout = captured
    main()
    sys.stdout = sys.__stdout__
    assert "Error: Unknown operator" in captured.getvalue()

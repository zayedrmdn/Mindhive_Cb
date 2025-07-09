"""
Part 3: Tool Calling Tests
Objective: Integrate and test the calculator tool.
"""

import requests
import pytest

BASE = "http://127.0.0.1:8000"

def test_calculator_success():
    r = requests.get(f"{BASE}/api/calculate", params={"a":5, "b":3, "op":"add"})
    print("Calculator Success Response:", r.json())
    assert r.status_code == 200
    assert r.json()["result"] == 8.0

def test_calculator_divide_by_zero():
    r = requests.get(f"{BASE}/api/calculate", params={"a":10, "b":0, "op":"div"})
    print("Calculator DivZero Response:", r.text)
    assert r.status_code == 400
    assert "Division by zero" in r.json()["detail"]

"""
Part 5: Unhappy Flows Tests
Objective: Ensure robustness against invalid or malicious inputs.
"""

import requests
import pytest

BASE = "http://127.0.0.1:8000"

def test_products_missing_param():
    r = requests.get(f"{BASE}/api/products")
    print("Products Missing Param Response:", r.text)
    assert r.status_code == 422

def test_outlets_missing_param():
    r = requests.get(f"{BASE}/api/outlets")
    print("Outlets Missing Param Response:", r.text)
    assert r.status_code == 422

def test_outlets_downtime_simulation():
    r = requests.get(f"{BASE}/api/outlets", params={"query":"trigger500"})
    print("Outlets Downtime Simulated Response:", r.text)
    assert r.status_code == 500
    assert "Simulated server error" in r.json()["detail"]

def test_outlets_sql_injection_safety():
    inj = "1';DROP TABLE outlets;--"
    r = requests.get(f"{BASE}/api/outlets", params={"query":inj})
    print("SQL Injection Response:", r.json())
    assert r.status_code == 200
    assert isinstance(r.json().get("outlets"), list)

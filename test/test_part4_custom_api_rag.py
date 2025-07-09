"""
Part 4: Custom API & RAG Integration Tests
Objective: Validate /products (FAISS) and /outlets (Text2SQL).
"""

import requests
import pytest

BASE = "http://127.0.0.1:8000"

def test_products_endpoint():
    r = requests.get(f"{BASE}/api/products", params={"query":"ceramic"})
    print("Products Response:", r.json())
    assert r.status_code == 200
    assert isinstance(r.json().get("products"), list)
    assert len(r.json()["products"]) > 0

def test_outlets_endpoint():
    r = requests.get(f"{BASE}/api/outlets", params={"query":"Petaling Jaya"})
    print("Outlets Response:", r.json())
    assert r.status_code == 200
    assert isinstance(r.json().get("outlets"), list)
    assert len(r.json()["outlets"]) > 0

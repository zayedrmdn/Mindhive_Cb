# test/test_memory.py
import os
import requests
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE = "http://127.0.0.1:8000/api/chat"
HEADERS = {"Content-Type": "application/json"}

@pytest.fixture(scope="module", autouse=True)
def check_server():
    # ensure server is up before tests
    r = requests.get("http://127.0.0.1:8000/")
    assert r.status_code == 200
    return True

def test_memory_sequence():
    # Turn 1
    r1 = requests.post(BASE, headers=HEADERS, json={"message": "Hello"})
    assert r1.status_code == 200
    assert "Hello" in r1.json()["response"]

    # Turn 2
    r2 = requests.post(BASE, headers=HEADERS, json={"message": "What can you do?"})
    assert r2.status_code == 200
    assert "help" in r2.json()["response"].lower()

    # Turn 3
    r3 = requests.post(BASE, headers=HEADERS, json={"message": "What did I say first?"})
    assert r3.status_code == 200
    # should echo your first turn
    assert "Hello" in r3.json()["response"]

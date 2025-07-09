# test/test_part2_agentic_planning.py

import requests

BASE = "http://127.0.0.1:8000/api/agent"

def test_agent_arithmetic_routing():
    """
    Part 2: Agentic Planning.
    The agent should parse an arithmetic query and call the calculator.
    """
    r = requests.post(BASE, json={"message": "Calculate 7 + 6"})
    print("Arithmetic Routing →", r.status_code, r.json())
    assert r.status_code == 200
    data = r.json()
    # we know the calculator returns a top‐level 'result' key
    assert "result" in data
    assert data["result"] == 13.0

def test_agent_fallback_to_chat():
    """
    If the message is not arithmetic/product/outlet, it should fallback to chat.
    """
    r = requests.post(BASE, json={"message": "Hello there"})
    print("Fallback Chat →", r.status_code, r.json())
    assert r.status_code == 200
    data = r.json()
    assert "response" in data

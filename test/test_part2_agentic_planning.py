# test/test_part2_agentic_planning.py
import requests

BASE = "http://127.0.0.1:8000/api/agent"

def test_agent_arithmetic_routing():
    r = requests.post(BASE, json={"message": "Calculate 7 + 6"})
    assert r.status_code == 200
    data = r.json()
    assert "result" in data
    assert data["result"] == 13.0

def test_agent_fallback_to_chat():
    r = requests.post(BASE, json={"message": "Hello there"})
    assert r.status_code == 200
    data = r.json()
    assert "response" in data

def test_agent_product_routing():
    r = requests.post(BASE, json={"message": "Show me products for ceramic mugs"})
    assert r.status_code == 200
    data = r.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    assert len(data["products"]) > 0

def test_agent_outlet_routing():
    r = requests.post(BASE, json={"message": "Any outlets in Petaling Jaya?"})
    assert r.status_code == 200
    data = r.json()
    assert "outlets" in data
    assert isinstance(data["outlets"], list)
    assert len(data["outlets"]) > 0

def test_agent_missing_info_outlet():
    r = requests.post(BASE, json={"message": "Is there an outlet?"})
    assert r.status_code == 200
    data = r.json()
    # should get a follow-up prompt
    assert "response" in data
    reply = data["response"].lower()
    assert "specify" in reply or "which" in reply

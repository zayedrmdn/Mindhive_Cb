# test/test_part1_sequential_conversation.py
import importlib
import requests

ma = importlib.import_module("app.memory_agent")

BASE = "http://127.0.0.1:8000/api/chat"

def clear_history():
    # keep the same list object that controller.py uses, just empty it
    ma.history.clear()

def test_part1_three_turns():
    clear_history()
    msgs = ["Hello", "How are you today?", "What did I say first?"]
    for m in msgs:
        r = requests.post(BASE, json={"message": m})
        assert r.status_code == 200
        assert "response" in r.json()
    assert "hello" in r.json()["response"].lower()

def test_part1_interrupted_context():
    clear_history()

    # set a fact
    r = requests.post(BASE, json={"message": "My favourite drink is a latte"})
    assert r.status_code == 200

    # simulate a fresh session
    clear_history()

    # ask about the forgotten fact
    r = requests.post(BASE, json={"message": "What is my favourite drink?"})
    assert r.status_code == 200
    data = r.json()
    assert "response" in data
    assert data["response"].strip() != ""   # bot replied without crashing

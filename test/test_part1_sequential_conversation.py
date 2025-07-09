# test/test_part1_sequential_conversation.py

import requests

BASE = "http://127.0.0.1:8000/api/chat"

def test_part1_three_turns():
    """
    Part 1: Sequential Conversation.
    Send three related turns and assert we always get a 200 and a 'response' key.
    """
    messages = [
        "Hello",
        "How are you today?",
        "What did I say first?"
    ]
    for msg in messages:
        r = requests.post(BASE, json={"message": msg})
        print(f"Sent: {msg!r}, Got:", r.status_code, r.json())
        assert r.status_code == 200
        data = r.json()
        assert "response" in data

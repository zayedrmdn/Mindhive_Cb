# scripts/create_outlets_db.py
import sqlite3
import os

DB_PATH = "data/outlets.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS outlets(
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    hours TEXT
)""")
# sample rows
rows = [
    (1, "ZUS Coffee SS2", "Petaling Jaya", "9:00 AM–8:00 PM"),
    (2, "ZUS Coffee KLCC", "Kuala Lumpur", "8:00 AM–9:00 PM"),
    (3, "ZUS Coffee Bangsar", "Kuala Lumpur", "7:30 AM–7:00 PM")
]
c.executemany("INSERT OR IGNORE INTO outlets VALUES (?,?,?,?)", rows)
conn.commit()
conn.close()
print("Outlets DB ready")

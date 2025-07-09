# app/outlets_api.py
from fastapi import APIRouter, Query, HTTPException
import sqlite3

router = APIRouter(tags=["outlets"])
DB_PATH = "data/outlets.db"

@router.get("/outlets")
def read_outlets(query: str = Query(..., description="Natural language filter, e.g. city name")):

    if "trigger500" in query.lower():
        raise HTTPException(status_code=500, detail="Simulated server error")
    
    # Very basic “NL→SQL” mapping: check for city keywords
    city = None
    text = query.lower()
    for possible in ["kuala lumpur", "petaling jaya", "bangsar"]:
        if possible in text:
            city = possible.title()
            break

    sql = "SELECT * FROM outlets"
    params = ()
    if city:
        sql += " WHERE city = ?"
        params = (city,)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute(sql, params)
        cols = [c[0] for c in cursor.description]
        rows = [dict(zip(cols, r)) for r in cursor.fetchall()]
        conn.close()
        return {"outlets": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# app/controller.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.memory_agent import chat_with_memory
from app.calculator import calculate as calc
from app.products_api import read_products
from app.outlets_api import read_outlets

router = APIRouter()

# --- Part 1 chat endpoint ---
class ChatRequest(BaseModel):
    message: str

@router.post("/chat", tags=["chat"])
def chat_endpoint(req: ChatRequest):
    """Sequential conversation with memory."""
    try:
        return {"response": chat_with_memory(req.message)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Part 2 agentic planner endpoint ---
class AgentRequest(BaseModel):
    message: str

@router.post("/agent", tags=["agent"])
def agent_endpoint(req: AgentRequest):
    """
    Agentic planning: parse intent, call appropriate tool or fallback to chat.
    """
    text = req.message.lower().strip()

    # 1. Arithmetic intent
    if any(op in text for op in ["add", "sub", "multiply", "divide", "+", "-", "*", "/"]):
        # crude parse: find two numbers
        tokens = text.replace("?", "").replace(",", "").split()
        nums = [t for t in tokens if t.replace(".", "", 1).isdigit()]
        if len(nums) >= 2:
            a, b = float(nums[0]), float(nums[1])
            if "add" in text or "+" in text:
                op = "add"
            elif "sub" in text or "-" in text:
                op = "sub"
            elif "multiply" in text or "*" in text:
                op = "mul"
            elif "divide" in text or "/" in text:
                op = "div"
            else:
                raise HTTPException(status_code=400, detail="Could not determine operation")
            return calc(a=a, b=b, op=op)
        raise HTTPException(status_code=400, detail="Need two numbers to calculate")

    # 2. Product-KB intent
    if "product" in text or "drinkware" in text:
        # forward the raw text as the query parameter
        return read_products(query=req.message)

    # 3. Outlets intent
    if "outlet" in text:
        return read_outlets(query=req.message)

    # 4. Fallback to chat memory
    return {"response": chat_with_memory(req.message)}

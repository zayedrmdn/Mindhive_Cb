# app/controller.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.memory_agent import chat_with_memory
from app.calculator import calculate as calc
from app.products_api import read_products, docs as PRODUCT_DOCS
from app.outlets_api import read_outlets

router = APIRouter()

# ---------- Part 1 : Sequential Conversation --------------------------------
class ChatRequest(BaseModel):
    message: str

@router.post("/chat", tags=["chat"])
def chat_endpoint(req: ChatRequest):
    try:
        return {"response": chat_with_memory(req.message)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------- Part 2 : Agentic Planner ----------------------------------------
class AgentRequest(BaseModel):
    message: str

@router.post("/agent", tags=["agent"])
def agent_endpoint(req: AgentRequest):
    """
    Planner flow:
    1. Arithmetic  → /calculate
    2. Product     → /products  (fallback to local keyword filter on ANY failure)
    3. Outlet      → follow-up if no location, else /outlets
    4. Fallback    → chat
    """
    text = req.message.lower().strip()

    # 1. Arithmetic intent ----------------------------------------------------
    if any(op in text for op in ["add", "sub", "multiply", "divide", "+", "-", "*", "/"]):
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

    # 2. Product-KB intent ----------------------------------------------------
    if "product" in text or "drinkware" in text:
        try:
            return read_products(query=req.message)
        except Exception:
            # Any error → simple keyword fallback
            hits = []
            for d in PRODUCT_DOCS:
                combined = f"{d['title']} {d['description']}".lower()
                if any(tok in combined for tok in text.split()):
                    hits.append(d)
            return {"products": hits[:3] or PRODUCT_DOCS[:3]}

    # 3. Outlet intent --------------------------------------------------------
    if "outlet" in text:
        stripped = text.rstrip("?.!").strip()
        if stripped in {"is there an outlet", "any outlet", "any outlets"}:
            return {"response": "Sure — could you specify which location or area you mean?"}
        return read_outlets(query=req.message)

    # 4. Fallback to chat -----------------------------------------------------
    return {"response": chat_with_memory(req.message)}

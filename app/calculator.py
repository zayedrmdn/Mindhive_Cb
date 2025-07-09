from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["calculator"])

@router.get("/calculate")
def calculate(
    a: float = Query(...), 
    b: float = Query(...), 
    op: str = Query("add")
):
    if op == "add":
        result = a + b
    elif op == "sub":
        result = a - b
    elif op == "mul":
        result = a * b
    elif op == "div":
        if b == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        result = a / b
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported op '{op}'")
    return {"a": a, "b": b, "op": op, "result": result}

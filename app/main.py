from fastapi import FastAPI
from app.calculator import router as calculator_router
from app.products_api import router as products_router
from app.outlets_api import router as outlets_router
from app.controller import router as controller_router   # ← this
from app.controller import router as agent_router


app = FastAPI(title="Mindhive Chatbot Assessment API")

app.include_router(calculator_router, prefix="/api")
app.include_router(products_router,   prefix="/api")
app.include_router(outlets_router,    prefix="/api")
app.include_router(controller_router, prefix="/api")    # ← and this
app.include_router(agent_router,      prefix="/api")


@app.get("/")
def root():
    return {"message": "API running"}

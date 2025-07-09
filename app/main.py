from fastapi import FastAPI
from app.calculator import router as calculator_router
from app.products_api import router as products_router
from app.outlets_api import router as outlets_router
from app.controller import router as controller_router   # ← this
from app.controller import router as agent_router
from fastapi.responses import HTMLResponse



app = FastAPI(title="Mindhive Chatbot Assessment API")

app.include_router(calculator_router, prefix="/api")
app.include_router(products_router,   prefix="/api")
app.include_router(outlets_router,    prefix="/api")
app.include_router(controller_router, prefix="/api")    # ← and this
app.include_router(agent_router,      prefix="/api")


@app.get("/")
def root():
    return {"message": "API running"}

@app.get("/", response_class=HTMLResponse)
def landing():
    return """
    <h1>Mindhive Chatbot API – Demo</h1>
    <p>This backend powers the Mindhive Chatbot Engineer assessment.</p>
    <ul>
        <li><a href="/docs">OpenAPI docs (Swagger UI)</a></li>
        <li><a href="/api/products?query=ceramic">/api/products example</a></li>
        <li><a href="/api/outlets?query=Petaling%20Jaya">/api/outlets example</a></li>
        <li><a href="/api/calculate?a=2&b=3&op=add">/api/calculate example</a></li>
    </ul>
    """
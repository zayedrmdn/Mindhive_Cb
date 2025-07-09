# app/products_api.py
import os, json
from fastapi import APIRouter, Query, HTTPException
from huggingface_hub import InferenceClient


router = APIRouter(tags=["products"])

# Load product docs once
with open("data/product_map.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("Missing HUGGINGFACEHUB_API_TOKEN")

client   = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"

@router.get("/products")
def read_products(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(3, ge=1, le=10)
):
    # Build document corpus
    texts = [f"{d['title']}. {d['description']}" for d in docs]

    try:
        # Two positional args: source_sentence, other_sentences
        scores = client.sentence_similarity(query, texts, model=MODEL_ID)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Hugging Face similarity API error: {e}")

    # Pair scores with docs, sort, and return top_k
    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)[:top_k]
    results = [
        {
            "id": doc["id"],
            "title": doc["title"],
            "description": doc["description"],
            "score": float(score)
        } for score, doc in ranked
    ]
    return {"products": results}

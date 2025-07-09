# app/products_api.py
from fastapi import APIRouter, Query, HTTPException
import json
import numpy as np
from sentence_transformers import SentenceTransformer

router = APIRouter(tags=["products"])

# Paths and embedding model
MAP_PATH  = "data/product_map.json"
EMB_MODEL = "all-MiniLM-L6-v2"

# Preload your product docs and embedder (these are lightweight enough)
with open(MAP_PATH, "r", encoding="utf-8") as f:
    docs = json.load(f)
embedder = SentenceTransformer(EMB_MODEL)

@router.get("/products")
def read_products(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(3, ge=1, le=10)
):
    """
    FAISS index is loaded on-demand inside this function to avoid
    eating RAM at startup on low-memory environments.
    """
    try:
        import faiss  # delay FAISS import until endpoint is hit
        INDEX_PATH = "data/faiss_index.idx"
        index = faiss.read_index(INDEX_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading vector index: {e}")

    # Embed the incoming query
    q_emb = embedder.encode([query], convert_to_numpy=True)

    # Run the similarity search
    D, I = index.search(q_emb, top_k)

    # Build results
    results = []
    for idx in I[0]:
        if idx < 0 or idx >= len(docs):
            continue
        d = docs[idx]
        results.append({
            "id":          d["id"],
            "title":       d["title"],
            "description": d["description"]
        })

    return {"products": results}

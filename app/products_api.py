# app/products_api.py
from fastapi import APIRouter, Query
import faiss, json
import numpy as np
from sentence_transformers import SentenceTransformer

router = APIRouter(tags=["products"])

# load index and docs
INDEX_PATH = "data/faiss_index.idx"
MAP_PATH   = "data/product_map.json"
EMB_MODEL  = "all-MiniLM-L6-v2"

index = faiss.read_index(INDEX_PATH)
with open(MAP_PATH, "r", encoding="utf-8") as f:
    docs = json.load(f)

embedder = SentenceTransformer(EMB_MODEL)

@router.get("/products")
def read_products(query: str = Query(..., description="Search query"),
                  top_k: int = Query(3, ge=1, le=10)):
    # embed query
    q_emb = embedder.encode([query], convert_to_numpy=True)
    # search
    D, I = index.search(q_emb, top_k)
    results = []
    for idx in I[0]:
        doc = docs[idx]
        results.append({
            "id": doc["id"],
            "title": doc["title"],
            "description": doc["description"]
            # you could add a simple summary here if desired
        })
    return {"products": results}

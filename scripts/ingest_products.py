# scripts/ingest_products.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# paths
DATA_PATH = "data/product_docs.json"
INDEX_PATH = "data/faiss_index.idx"
EMB_MODEL = "all-MiniLM-L6-v2"

# load docs
with open(DATA_PATH, "r", encoding="utf-8") as f:
    docs = json.load(f)

# initialize embedder
embedder = SentenceTransformer(EMB_MODEL)

# embed descriptions
texts = [d["title"] + ". " + d["description"] for d in docs]
embs = embedder.encode(texts, convert_to_numpy=True)

# build FAISS index
d = embs.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embs)
os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
faiss.write_index(index, INDEX_PATH)

# save mapping from idx→doc
with open("data/product_map.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, indent=2)

print(f"Indexed {len(docs)} documents")

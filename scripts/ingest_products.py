# scripts/ingest_products.py
import json
import os

# paths
DATA_PATH = "data/product_docs.json"
OUTPUT_PATH = "data/product_map.json"

def main():
    # ensure output folder exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # load the raw docs
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        docs = json.load(f)

    # write them straight through as the map
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)

    print(f"Wrote {len(docs)} documents to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

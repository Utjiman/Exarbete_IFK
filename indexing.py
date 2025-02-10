import os
import json
import numpy as np
import hnswlib
from sentence_transformers import SentenceTransformer


PROCESSED_DIR = "data/processed"
INDEX_DIR = "data/index"

# Ladda in modellen för att skapa vektorer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initiera HNSWlib index
dimension = 384  # All-MiniLM-L6-v2 ger vektorer med 384 dimensioner
num_elements = 0  # Vi räknar antal element

index = hnswlib.Index(space="cosine", dim=dimension)
index.init_index(max_elements=10000, ef_construction=200, M=16)
index.set_ef(50)  # Kontroll över sökprecision

texts = []  # Lista för att lagra texter som ska lagras direkt i vektorerna


for filename in os.listdir(PROCESSED_DIR):
    if filename.endswith("_chunks.json"):
        filepath = os.path.join(PROCESSED_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        for chunk in chunks:
            texts.append(chunk["text"])
            num_elements += 1

# Skapa vektorer av alla texter
vectors = model.encode(texts, show_progress_bar=True)

index.add_items(vectors, np.arange(num_elements))

index.save_index(os.path.join(INDEX_DIR, "ifk_index.bin"))

print(f"✅ Indexering klar! Sparade {num_elements} chunkar i {INDEX_DIR}/ifk_index.bin")

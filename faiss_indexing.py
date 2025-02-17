import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Filvägar
PROCESSED_DIR = "data/processed"
INDEX_PATH = "data/index/ifk_faiss_index.index"

# Ladda embedding-modellen
model = SentenceTransformer("intfloat/multilingual-e5-large")

# Skapa en Faiss index
dim = 1024  # Dimensionen för embeddings
index = faiss.IndexFlatL2(dim)

# För att hålla koll på globalt unika chunk-id
global_chunk_id = 0

# För att spara chunkar och deras motsvarande id:n
chunk_data = []

# Läs och bearbeta alla JSON-filer i processed-mappen
for filename in os.listdir(PROCESSED_DIR):
    if filename.endswith("_chunks.json"):
        file_path = os.path.join(PROCESSED_DIR, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        print(f"📂 Bearbetar {filename} ({len(chunks)} chunks)...")

        for chunk in chunks:
            # Om chunken har en lista med matcher (för matches, records etc.)
            if isinstance(chunk, dict) and "matches" in chunk:
                chunk_text = json.dumps(chunk["matches"])  # Vi använder JSON-sträng för hela listan
            elif isinstance(chunk, dict) and "text" in chunk:
                chunk_text = chunk["text"]
            elif isinstance(chunk, str):
                chunk_text = chunk
            else:
                print(f"⚠️ Skipping invalid chunk format: {type(chunk)}")
                continue

            # Skapa embedding för chunk-texten
            embedding = model.encode(chunk_text, convert_to_numpy=True)

            # Lägg till den i Faiss-indexet
            index.add(np.array([embedding]))

            # Spara chunk och dess id
            chunk_data.append({"chunk_id": global_chunk_id, "text": chunk_text})

            # Öka global_chunk_id för nästa chunk
            global_chunk_id += 1

# Spara Faiss-indexet
faiss.write_index(index, INDEX_PATH)

# Spara chunk_data till en fil för framtida referens
with open("data/index/chunk_data.json", "w", encoding="utf-8") as f:
    json.dump(chunk_data, f, indent=4, ensure_ascii=False)

print(f"✅ Indexering klar! {global_chunk_id} chunkar indexerade.")

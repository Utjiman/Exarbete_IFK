import os
import json
import hnswlib
import numpy as np
from sentence_transformers import SentenceTransformer

# Filvägar
PROCESSED_DIR = "data/processed"
INDEX_DIR = "data/index"
INDEX_PATH = os.path.join(INDEX_DIR, "ifk_index.bin")
CHUNK_MAPPING_PATH = os.path.join(INDEX_DIR, "chunk_mapping.json")

# Se till att index-mappen finns
os.makedirs(INDEX_DIR, exist_ok=True)

# Radera gamla indexfiler om de finns (för att undvika konflikt)
if os.path.exists(INDEX_PATH):
    os.remove(INDEX_PATH)
if os.path.exists(CHUNK_MAPPING_PATH):
    os.remove(CHUNK_MAPPING_PATH)

# Ladda SentenceTransformer för att skapa embeddingar
model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

# Skapa ett nytt HNSWLib index
p = hnswlib.Index(space="cosine", dim=768)
p.init_index(max_elements=20000, ef_construction=400, M=32)

# Håller reda på chunk-id och mapping
chunk_mapping = {}
global_index = 0

print("🔄 Läser in och indexerar chunk-filer...")

# Läs och bearbeta alla JSON-filer i processed-mappen
for filename in os.listdir(PROCESSED_DIR):
    if filename.endswith("_chunks.json"):
        file_path = os.path.join(PROCESSED_DIR, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        print(f"📂 Bearbetar {filename} ({len(chunks)} chunks)...")

        # Se till att varje chunk är en sträng innan vi skapar embeddingar
        for chunk in chunks:
            if isinstance(chunk, dict):
                if "text" in chunk:
                    chunk_text = chunk["text"]
                elif "matches" in chunk:
                    # 🏆 Hantera matcher genom att konkatenera deras info
                    chunk_text = "\n".join(
                        [f"{m['Datum']} | {m['Matchtyp']} | {m['Match']} | {m['Resultat']} | {m['Spelplats']} | {m['Publik']} pers"
                         for m in chunk["matches"]]
                    )
                else:
                    print(f"⚠️ Okänt chunk-format i {filename}, hoppar över...")
                    continue
            elif isinstance(chunk, str):
                chunk_text = chunk
            else:
                print(f"⚠️ Skipping invalid chunk format: {type(chunk)}")
                continue

            # ✅ Lägg till chunken i mapping
            chunk_mapping[str(global_index)] = chunk_text

            # 🔥 Debug (visa endast var 100:e chunk)
            if global_index % 100 == 0:
                print(f"✅ Indexerar chunk {global_index}: {chunk_text[:100]}...")

            # Skapa embedding och lägg till i indexet
            embedding = model.encode(chunk_text, convert_to_numpy=True)
            p.add_items(np.array([embedding]), np.array([global_index], dtype=np.int32))

            global_index += 1

# Spara indexet
print("💾 Sparar index...")
p.save_index(INDEX_PATH)

# Spara chunk_mapping som JSON
with open(CHUNK_MAPPING_PATH, "w", encoding="utf-8") as f:
    json.dump(chunk_mapping, f, indent=4, ensure_ascii=False)

print(f"✅ Indexering klar! {global_index} chunkar indexerade.")
print("Antal chunkar i index:", p.get_current_count())

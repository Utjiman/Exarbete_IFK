import hnswlib
import json
import numpy as np

# Filvägar
INDEX_PATH = "data/index/ifk_index.bin"
CHUNK_MAPPING_PATH = "data/index/chunk_mapping.json"

# Ladda index
p = hnswlib.Index(space="cosine", dim=384)
p.load_index(INDEX_PATH)

# Ladda chunk-mapping
with open(CHUNK_MAPPING_PATH, "r", encoding="utf-8") as f:
    chunk_mapping = json.load(f)

print(f"✅ Indexet är laddat! Antal poster: {p.get_current_count()}")
print(f"🔍 Antal chunkar i mapping: {len(chunk_mapping)}")

# Debug: Skriv ut de första 5 chunkarna
for i in range(min(5, len(chunk_mapping))):
    print(f"🔹 Chunk {i}: {chunk_mapping[str(i)][:200]}...")

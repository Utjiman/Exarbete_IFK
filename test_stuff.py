import hnswlib
import numpy as np
from sentence_transformers import SentenceTransformer
import json

# Ladda in chunk-mappningen
with open("data/index/chunk_mapping.json", "r", encoding="utf-8") as f:
    chunk_mapping = json.load(f)

# Ladda in embedding-modellen (samma som vid indexering)
model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")

# Ladda in indexet
p = hnswlib.Index(space="cosine", dim=768)
p.load_index("data/index/ifk_index.bin")  # Byt ut om index-filen har annat namn

# Lista med testfrågor för olika datasets
test_questions = [
    "Hur många gånger har IFK Göteborg vunnit Svenska Cupen?",  # Ska hämta rekord
    "Vilka tränare har IFK Göteborg haft?",  # Ska hämta tränare
    "Hur många matcher har IFK Göteborg spelat i Allsvenskan?",  # Ska hämta matcher
    "Vem är IFK Göteborgs bästa målskytt genom tiderna?"  # Ska hämta spelare
]

# Loopa genom testfrågorna och kolla retrieval
for question in test_questions:
    query_embedding = model.encode(question)
    query_embedding = np.array([query_embedding], dtype=np.float32)

    labels, distances = p.knn_query(query_embedding, k=5)
    retrieved_chunks = [chunk_mapping[str(i)] for i in labels[0]]

    print(f"\n🔎 Fråga: {question}")
    for i, chunk in enumerate(retrieved_chunks):
        print(f"Chunk {labels[0][i]}:\n{chunk[:300]}...\n")

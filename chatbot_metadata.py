import os
import faiss
import numpy as np
import json
import requests
from sentence_transformers import SentenceTransformer

PROCESSED_DIR = "data/processed_metadata"
INDEX_PATH = "data/index/ifk_faiss_index_metadata.index"


model = SentenceTransformer("intfloat/multilingual-e5-large")


dim = 1024  
index = faiss.read_index(INDEX_PATH)


chunk_data = []
for filename in os.listdir(PROCESSED_DIR):
    if filename.endswith("_metadata_chunks.json"):
        with open(os.path.join(PROCESSED_DIR, filename), "r", encoding="utf-8") as f:
            chunk_data.extend(json.load(f))

def embed_text(text):
    """ Skapa en embedding av texten för frågan """
    return model.encode(text, normalize_embeddings=True)

def search_index(query, top_k=10):
    """ Söker i Faiss-index och hämtar chunkar med metadata från JSON-filerna """
    query_vector = embed_text(query)
    query_vector = np.array([query_vector]).astype("float32")

    
    distances, indices = index.search(query_vector, top_k)

    print(f"🔎 Rådata från Faiss")
    print(f"   - Distances: {distances}")
    print(f"   - Indices: {indices}")

    indices = [int(idx) for idx in indices[0]]  

    results = []
    for idx in indices:
        if idx < len(chunk_data):
            chunk = chunk_data[idx]
            chunk_text = chunk["text"] if "text" in chunk else json.dumps(chunk, ensure_ascii=False)
            metadata = chunk.get("metadata", {})
            print(f"🔹 Hittad chunk {idx}: {chunk_text[:400]}... med metadata: {metadata}")
            results.append({"text": chunk_text, "metadata": metadata})

    if not results:
        print("❌ Inga relevanta chunks hittades!")

    return results

def ask_lm_studio(question, max_tokens=500, temperature=0.3):
    """ Ställ en fråga och skicka relevanta chunks med metadata till LM Studio """
    retrieved_chunks = search_index(question)

    if not retrieved_chunks:
        return "Jag vet inte."

    context = "\n".join([f"Text: {chunk['text']} | Metadata: {chunk['metadata']}" for chunk in retrieved_chunks[:10]])


    prompt = f"""
    Du är en expert på IFK Göteborg.
    Använd **endast** den givna informationen för att svara på frågan.  
    Om svaret inte finns i texten, säg exakt: "Jag vet inte."  
    Använd **exakta ord** från texten och metadata och spekulera aldrig.

    **Information:**  
    {context}

    **Fråga:** {question}

    **Svara enbart med exakt information från texten och metadata.**  
    Exempel på format:  
    - "Enligt datan har Mikael Nilsson spelat flest matcher i Champions League: 44"  
    - "Jag vet inte."
    
    **Svar:**
    """

    response = requests.post(
        "http://localhost:1234/v1/completions",
        json={
            "model": "mistral-7b-instruct-v0.2",
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature  
        },
    )

    try:
        return response.json()["choices"][0]["text"].strip()
    except Exception as e:
        return f"Fel vid anrop till LM Studio: {str(e)}"

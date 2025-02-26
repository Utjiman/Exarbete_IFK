import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


PROCESSED_DIR = "data/processed_metadata"  
INDEX_PATH = "data/index/ifk_faiss_index_metadata.index"  
CHUNK_DATA_PATH = "data/index/chunk_data_metadata.json" 


model = SentenceTransformer("intfloat/multilingual-e5-large")


dim = 1024  
index = faiss.IndexFlatL2(dim)


global_chunk_id = 0


chunk_data = []


for filename in os.listdir(PROCESSED_DIR):
    if filename.endswith("_chunks.json"): 
        file_path = os.path.join(PROCESSED_DIR, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        print(f"📂 Bearbetar {filename} ({len(chunks)} chunks)...")

        for chunk in chunks:
            
            if "text" in chunk:  
                chunk_text = chunk["text"]
            elif "matches" in chunk:  
                chunk_text = json.dumps(chunk["matches"])  
            elif "record" in chunk:  
                chunk_text = chunk["record"]
            else:
                print(f"⚠️ Chunk {chunk.get('chunk_id', 'okänt ID')} har inte förväntad struktur (text/matches/record).")
                continue  

            
            embedding = model.encode(chunk_text, convert_to_numpy=True)

            
            index.add(np.array([embedding]))

            
            chunk_data.append({
                "chunk_id": chunk["chunk_id"],
                "text": chunk_text,
                "metadata": chunk.get("metadata", {})
            })

            
            global_chunk_id += 1


faiss.write_index(index, INDEX_PATH)


with open(CHUNK_DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(chunk_data, f, indent=4, ensure_ascii=False)

print(f"✅ Ny indexering klar! {global_chunk_id} chunkar indexerade med metadata.")

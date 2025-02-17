import os
import pandas as pd
import json

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
CHUNK_SIZE = 500  
OVERLAP = 50  



def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    words = text.split()  
    chunks = []
    
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap  

    return chunks

for filename in os.listdir(RAW_DIR):
    if filename.endswith(".csv"):  
        filepath = os.path.join(RAW_DIR, filename)
        print(f"🔄 Bearbetar {filename}...")

       
        df = pd.read_csv(filepath)

       
        text_data = " ".join(df.astype(str).sum(axis=1))

        
        chunks = chunk_text(text_data, chunk_size=CHUNK_SIZE, overlap=OVERLAP)

        
        chunked_data = [{"chunk_id": i, "text": chunk} for i, chunk in enumerate(chunks)]

        
        output_filename = filename.replace("_raw.csv", "_chunks.json")
        output_path = os.path.join(PROCESSED_DIR, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunked_data, f, ensure_ascii=False, indent=4)

        print(f"✅ Chunkning klar för {filename}! Sparad som {output_filename}")

print("✅ Alla filer har bearbetats och chunkats!")

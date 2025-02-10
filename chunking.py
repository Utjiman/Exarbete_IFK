import os
import pandas as pd
import json

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

def chunk_text(text, chunk_size=1000):
    words = text.split()  
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

for filename in os.listdir(RAW_DIR):
    if filename.endswith(".csv"):  
        filepath = os.path.join(RAW_DIR, filename)
        print(f"🔄 Bearbetar {filename}...")

        # Läs in CSV-fil
        df = pd.read_csv(filepath)

        # Slå ihop alla textfält till en lång textsträng
        text_data = " ".join(df.astype(str).sum(axis=1))

        # Dela upp texten i chunks på 1000 ord
        chunks = chunk_text(text_data, chunk_size=1000)

        # Skapa en lista med chunkad data
        chunked_data = [{"chunk_id": i, "text": chunk} for i, chunk in enumerate(chunks)]

        # Spara som JSON-fil i processed-mappen
        output_filename = filename.replace("_raw.csv", "_chunks.json")
        output_path = os.path.join(PROCESSED_DIR, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunked_data, f, ensure_ascii=False, indent=4)

        print(f"Chunkning klar för {filename}! Sparad som {output_filename}")

print("Alla filer har bearbetats och chunkats!")

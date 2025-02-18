import re
import json

# Läs in raw-filen
with open("data/raw/ifk_records_raw.csv", "r", encoding="utf-8") as f:
    raw_text = f.read()

def split_records_by_category(text):
    """
    Dela upp texten i mindre chunkar baserat på nyckelord.
    """
    categories = re.split(r"(?=\bAntal|\bFlest|\bMinst|\bStörsta)", text)  # Dela vid dessa nyckelord
    return [cat.strip() for cat in categories if cat.strip()]  # Ta bort tomma delar

# Skapa nya chunkar
chunks = split_records_by_category(raw_text)

# Spara som JSON för indexering
chunk_data = [{"chunk_id": i, "text": chunk} for i, chunk in enumerate(chunks)]

# Spara chunk-filen
with open("data/processed/ifk_records_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunk_data, f, indent=4, ensure_ascii=False)

print(f"✅ Skapade {len(chunks)} nya chunkar för rekord!")

import json
import csv


input_file = "data/raw/ifk_coaches_raw.csv"
output_file = "data/processed/ifk_coaches_chunks.json"


coaches = []
with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  

    for row in reader:
        if len(row) < 3:
            continue  

        title = row[0].strip()
        name = row[1].strip()
        details = row[2].strip()

       
        coaches.append(f"Namn: {name}\nTitel: {title}\nDetaljer: {details}")


chunk_size = 5
chunks = [
    {
        "chunk_id": i // chunk_size,
        "text": "\n\n".join(coaches[i:i + chunk_size])
    }
    for i in range(0, len(coaches), chunk_size)
]

# 🔹 Spara till JSON-fil
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=4)

print(f"✅ Chunkad tränardata sparad till: {output_file}")

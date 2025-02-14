import pandas as pd
import json
import os
import html
import re  # Importera regex för att rensa spelplats

# Ladda rådata
raw_file_path = "data/raw/ifk_matches_raw.csv"
output_file_path = "data/processed/ifk_matches_chunks.json"

# Läs in CSV-filen
df = pd.read_csv(raw_file_path)

# 🟢 1️⃣ Rensa och konvertera "Publik"-kolumnen korrekt
df["Publik"] = (
    df["Publik"]
    .astype(str)
    .str.replace(" ", "")  # Ta bort mellanslag i publiksiffror
    .replace("nan", "0")  # Byt ut NaN
)
df["Publik"] = pd.to_numeric(df["Publik"], errors="coerce").fillna(0).astype(int)

# 🟢 2️⃣ Rensa "&nbsp;" och andra HTML-entiteter från "Match" och "Spelplats"
df["Match"] = df["Match"].apply(lambda x: html.unescape(str(x)))
df["Spelplats"] = df["Spelplats"].apply(lambda x: html.unescape(str(x)))

# 🟢 3️⃣ Fixa "Spelplats" genom att **rensa alla siffror i slutet** och extra mellanslag
df["Spelplats"] = df["Spelplats"].apply(lambda x: re.sub(r"\s*\d+(\s\d+)*$", "", x).strip())

# 🟢 4️⃣ Se till att "Omgång" är None istället för NaN
df["Omgång"] = df["Omgång"].apply(lambda x: str(x) if pd.notna(x) else None)

# 🟢 5️⃣ Skapa chunkar med 5 matcher per chunk
chunk_size = 5
chunks = [
    {"chunk_id": i, "matches": df.iloc[i * chunk_size : (i + 1) * chunk_size].to_dict(orient="records")}
    for i in range((len(df) + chunk_size - 1) // chunk_size)
]

# 🟢 6️⃣ Spara chunkarna som JSON
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print(f"✅ Matchdata har rensats och chunkats till {output_file_path}")

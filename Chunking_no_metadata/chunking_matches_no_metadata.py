import pandas as pd
import json
import os
import html
import re  


raw_file_path = "data/raw/ifk_matches_raw.csv"
output_file_path = "data/processed/ifk_matches_chunks.json"


df = pd.read_csv(raw_file_path)


df["Publik"] = (
    df["Publik"]
    .astype(str)
    .str.replace(" ", "")  
    .replace("nan", "0")  
)
df["Publik"] = pd.to_numeric(df["Publik"], errors="coerce").fillna(0).astype(int)


df["Match"] = df["Match"].apply(lambda x: html.unescape(str(x)))
df["Spelplats"] = df["Spelplats"].apply(lambda x: html.unescape(str(x)))


df["Spelplats"] = df["Spelplats"].apply(lambda x: re.sub(r"\s*\d+(\s\d+)*$", "", x).strip())


df["Omgång"] = df["Omgång"].apply(lambda x: str(x) if pd.notna(x) else None)


chunk_size = 5
chunks = [
    {"chunk_id": i, "matches": df.iloc[i * chunk_size : (i + 1) * chunk_size].to_dict(orient="records")}
    for i in range((len(df) + chunk_size - 1) // chunk_size)
]


os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print(f"✅ Matchdata har rensats och chunkats till {output_file_path}")

import pandas as pd
import json
import os
import html
import re


raw_file_path = "data/raw/ifk_matches_raw.csv"
output_file_path = "data/processed_metadata/ifk_matches_metadata_chunks.json"


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


df["År"] = pd.to_datetime(df["Datum"], format="%Y%m%d").dt.year


grouped = df.groupby("År")


chunks = []
chunk_counter = 0  

for year, group in grouped:
    chunk = {
        "chunk_id": chunk_counter,  
        "year": year,
        "matches": []
    }
    
    
    for _, row in group.iterrows():
        match_data = {
            "Datum": row["Datum"],
            "Matchtyp": row["Matchtyp"],
            "Omgång": row["Omgång"],
            "Match": row["Match"],
            "Resultat": row["Resultat"],
            "Spelplats": row["Spelplats"],
            "Publik": row["Publik"]
        }
        chunk["matches"].append(match_data)
    
    
    chunk_counter += 1
    chunks.append(chunk)


os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print(f"✅ Matchdata har grupperats per år och sparats till {output_file_path}")

import json
import csv
import re


input_file = "data/raw/ifk_coaches_raw.csv"
output_file = "data/processed_metadata/ifk_coaches_metadata_chunks.json"


coaches = []
with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  

    for index, row in enumerate(reader):
        if len(row) < 3:
            continue  

        title = row[0].strip()
        name = row[1].strip()
        details = row[2].strip()

       
        match_info = re.findall(r"(\d+)\s+matcher", details)
        
        
        season_info = re.findall(r"(\d+)\s+säsonger", details)

    
        year_info = re.findall(r"(\d{4}[-/]\d{2}-\d{4}[-/]\d{2}|\d{4}-\d{4})", title)

        
        matches = int(match_info[0]) if match_info else 0
        
        
        seasons = int(season_info[0]) if season_info else 1
        
       
        years = ", ".join(year_info) if year_info else "Ej specificerat"

        
        coaches.append({
            "chunk_id": index,  
            "text": f"Namn: {name}\nTitel: {title}\nDetaljer: {details}",
            "metadata": {
                "namn": name,
                "titel": title,
                "år": years,  
                "säsonger": seasons,  
                "matcher": matches
            }
        })


with open(output_file, "w", encoding="utf-8") as f:
    json.dump(coaches, f, ensure_ascii=False, indent=4)

print(f"✅ Chunkad tränardata med metadata sparad till: {output_file}")

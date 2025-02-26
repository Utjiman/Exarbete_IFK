import os
import json
import re


with open("data/raw/ifk_records_raw.csv", "r", encoding="utf-8") as f:
    raw_text = f.read()

def split_records_by_category(text):
    """
    Dela upp texten i mindre chunkar baserat på nyckelord.
    """
    categories = [
        "Säsonger i Allsvenskan", "Antal SM-guld", "Antal Svenska cupen-guld", "Antal UEFA-cup-titlar",
        "Antal gruppsegrar i Intertotocupen", "Ligasegrar", "Allsvenska ligasegrar", "Flest segrar i rad",
        "Flest obesegrade i rad", "Antal vunna matcher i Allsvenskan efter underläge i halvtid",
        "Största publiksiffra", "Största seger", "Flest säsonger i IFK Göteborg", "Flest matcher",
        "Flest tävlingsmatcher", "Flest allsvenska matcher", "Flest matcher i Svenska cupen", 
        "Flest Europacupmatcher", "Flest matcher i Champions League", "Flest matcher i UEFA-cupen", 
        "Flest matcher i Europa League", "Flest ligamatcher i rad", "Flest SM-guld", "Flest UEFA-cuptitlar", 
        "Flest Svenska cupen-titlar", "Rekordtransfer", "Flest sejouer i föreningen", "Äldste spelare", 
        "Flest mål", "Flest mål i tävlingsmatcher", "Flest mål av en egen produkt", "Flest mål av en utländsk spelare", 
        "Flest allsvenska mål", "Flest mål i Svenska cupen", "Flest Europacup-mål", "Bäst målsnitt", 
        "Flest mål i samma match", "Flest hattricks", "Flest mål på en säsong", "Flest mål en allsvensk säsong", 
        "Flest assist", "Flest assist av en utländsk spelare", "Flest assist i Allsvenskan", 
        "Flest assist i tävlingsmatcher", "Högst assistsnitt i Allsvenskan", "Högst poängsnitt i Allsvenskan", 
        "Högst vinstprocent i Allsvenskan", "Flest hållna nollor", "Minst insläppta mål per match", "Oftast utvisad", 
        "Oftast varnad i Allsvenskan", "Flest landskamper", "Flest landskamper av en egen produkt", 
        "Flest mål i landslaget", "Flest matcher som tränare", "Flest säsonger som tränare", "Högst poängsnitt"
    ]
    
    
    chunks = []
    category = None
    current_record = ""

    for line in text.splitlines():
        if any(line.startswith(cat) for cat in categories):
            if category: 
                chunks.append({
                    'chunk_id': len(chunks) + 1,
                    'category': category,
                    'record': current_record.strip()
                })
            
            category = next(cat for cat in categories if line.startswith(cat))
            current_record = line
        else:
            current_record += " " + line
    
    
    if category:
        chunks.append({
            'chunk_id': len(chunks) + 1,
            'category': category,
            'record': current_record.strip()
        })
    
    return chunks


chunks = split_records_by_category(raw_text)


output_dir = 'data/processed_metadata/'
os.makedirs(output_dir, exist_ok=True)


output_file_path = os.path.join(output_dir, "ifk_records_metadata_chunks.json")
with open(output_file_path, 'w', encoding="utf-8") as json_file:
    json.dump(chunks, json_file, ensure_ascii=False, indent=4)

print(f"Data sparades i {output_file_path} som JSON.")

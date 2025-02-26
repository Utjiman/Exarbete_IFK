import csv
import json


players = []
with open("data/raw/ifk_players_raw.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  

    for row in reader:
        name, years, matches, goals, allsv_matches, allsv_goals = row

        
        matches = "0" if matches.lower() == "okänt" else matches
        goals = "0" if goals.lower() == "okänt" else goals
        allsv_matches = "0" if allsv_matches.lower() == "okänt" else allsv_matches
        allsv_goals = "0" if allsv_goals.lower() == "okänt" else allsv_goals

        
        player_metadata = {
            "namn": name,
            "i_blåvitt": years,
            "matcher": int(matches),
            "mål": int(goals),
            "allsvenska_matcher": int(allsv_matches),
            "allsvenska_mål": int(allsv_goals)
        }

        
        player_text = f"Namn: {name}\nI Blåvitt: {years}\nMatcher: {matches}\nMål: {goals}\nAllsvenska Matcher: {allsv_matches}\nAllsvenska Mål: {allsv_goals}"

       
        player_chunk = {
            "chunk_id": len(players), 
            "text": player_text,
            "metadata": player_metadata
        }

        
        players.append(player_chunk)


with open("data/processed_metadata/ifk_players_metadata_chunks.json", "w", encoding="utf-8") as f:
    json.dump(players, f, indent=4, ensure_ascii=False)

print(f"✅ Skapade {len(players)} nya chunkar för spelare med metadata!")

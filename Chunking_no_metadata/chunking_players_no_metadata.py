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

        
        player_info = f"Namn: {name}\nI Blåvitt: {years}\nMatcher: {matches}\nMål: {goals}\nAllsvenska Matcher: {allsv_matches}\nAllsvenska Mål: {allsv_goals}"
        players.append(player_info)


chunk_size = 10
chunks = [players[i:i + chunk_size] for i in range(0, len(players), chunk_size)]


chunk_data = [{"chunk_id": i, "text": "\n\n".join(chunk)} for i, chunk in enumerate(chunks)]


with open("data/processed/ifk_players_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunk_data, f, indent=4, ensure_ascii=False)

print(f"✅ Skapade {len(chunks)} nya chunkar för spelare!")

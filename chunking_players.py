import csv
import json

# 🔹 Läs in raw-filen
players = []
with open("data/raw/ifk_players_raw.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # Hoppa över header-raden

    for row in reader:
        name, years, matches, goals, allsv_matches, allsv_goals = row
        
        # Om matcher/mål är "Okänt", sätt till 0
        matches = "0" if matches.lower() == "okänt" else matches
        goals = "0" if goals.lower() == "okänt" else goals

        # Skapa en formaterad text
        player_info = f"Namn: {name}\nI Blåvitt: {years}\nMatcher: {matches}\nMål: {goals}\nAllsvenska Matcher: {allsv_matches}\nAllsvenska Mål: {allsv_goals}"
        players.append(player_info)

# 🔹 Dela upp i chunkar (10 spelare per chunk)
chunk_size = 10
chunks = [players[i:i + chunk_size] for i in range(0, len(players), chunk_size)]

# 🔹 Skapa JSON-struktur för indexering
chunk_data = [{"chunk_id": i, "text": "\n\n".join(chunk)} for i, chunk in enumerate(chunks)]

# 🔹 Spara chunkarna
with open("data/processed/ifk_players_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunk_data, f, indent=4, ensure_ascii=False)

print(f"✅ Skapade {len(chunks)} nya chunkar för spelare!")

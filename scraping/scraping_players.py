import requests
from bs4 import BeautifulSoup
import pandas as pd



# URL till spelarsidan
BASE_URL = "https://ifkdb.se/listor/allaspelare"

# Skicka request och hämta HTML
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

# Lista för att lagra spelardata
players = []

# Hitta tabellen och loopa igenom raderna
table_rows = soup.select("table tr")[1:]  # Hoppa över rubrikerna

for row in table_rows:
    cols = row.find_all("td")

    if len(cols) >= 6:  # Se till att vi har alla nödvändiga kolumner
        name = cols[0].text.strip()  # Spelarnamn
        seasons = cols[1].text.strip()  # Säsonger
        matches = cols[2].text.strip().replace("?", "Okänt")  # Antal matcher
        goals = cols[3].text.strip() if cols[3].text.strip() else "0"  # Mål
        allsvenskan_matches = cols[4].text.strip() if cols[4].text.strip() else "0"  # Matcher i Allsvenskan
        allsvenskan_goals = cols[5].text.strip() if cols[5].text.strip() else "0"  # Mål i Allsvenskan

        # Lagra datan i en lista
        players.append({
            "Namn": name,
            "I Blåvitt": seasons,
            "Matcher": matches,
            "Mål": goals,
            "Allsvenska Matcher": allsvenskan_matches,
            "Allsvenska Mål": allsvenskan_goals
        })

# Konvertera till DataFrame och spara
df = pd.DataFrame(players)
df.to_csv("../data/raw/ifk_players_raw.csv", index=False)

print("✅ Skrapning klar! Sparade spelardata till data/processed/ifk_players.csv")

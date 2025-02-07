import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_URL = "https://ifkdb.se/listor/allamatcher"

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

matches = []

table_rows = soup.select("table tr")[1:]  # Hoppa över första raden (rubriker)

for row in table_rows:
    cols = row.find_all("td")

    if len(cols) >= 7:  # Se till att vi har tillräckligt med kolumner
        date = cols[0].text.strip()  # Datum
        match_type = cols[1].text.strip()  # Matchtyp (ex. Allsvenskan, Vänskapsmatch)
        round_number = cols[2].text.strip() if cols[2].text.strip() else "N/A"  # Omgång
        teams = cols[3].text.strip().replace("\xa0", " ")  # Match 
        result = cols[4].text.strip() if cols[4].text.strip() else "Ej spelad"  # Resultat
        venue = cols[5].text.strip()  # Spelplats
        attendance = cols[6].text.strip().replace(" ", "").replace("\xa0", "")  

        # Lagra datan i en lista
        matches.append({
            "Datum": date,
            "Matchtyp": match_type,
            "Omgång": round_number,
            "Match": teams,
            "Resultat": result,
            "Spelplats": venue,
            "Publik": attendance
        })


df = pd.DataFrame(matches)
df.to_csv("data/raw/ifk_matches_raw.csv", index=False)

print("Skrapning klar! Sparade matcher till data/raw/ifk_matches.csv")


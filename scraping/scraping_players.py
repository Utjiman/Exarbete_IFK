import requests
from bs4 import BeautifulSoup
import pandas as pd




BASE_URL = "https://ifkdb.se/listor/allaspelare"


response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")


players = []


table_rows = soup.select("table tr")[1:]  

for row in table_rows:
    cols = row.find_all("td")

    if len(cols) >= 6:  
        name = cols[0].text.strip()  
        seasons = cols[1].text.strip() 
        matches = cols[2].text.strip().replace("?", "Okänt")  
        goals = cols[3].text.strip() if cols[3].text.strip() else "0" 
        allsvenskan_matches = cols[4].text.strip() if cols[4].text.strip() else "0"  
        allsvenskan_goals = cols[5].text.strip() if cols[5].text.strip() else "0"  

        
        players.append({
            "Namn": name,
            "I Blåvitt": seasons,
            "Matcher": matches,
            "Mål": goals,
            "Allsvenska Matcher": allsvenskan_matches,
            "Allsvenska Mål": allsvenskan_goals
        })


df = pd.DataFrame(players)
df.to_csv("../data/raw/ifk_players_raw.csv", index=False)

print("✅ Skrapning klar! Sparade spelardata till data/processed/ifk_players.csv")

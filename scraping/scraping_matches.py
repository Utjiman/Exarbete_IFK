import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_URL = "https://ifkdb.se/listor/allamatcher"

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

matches = []

table_rows = soup.select("table tr")[1:]  

for row in table_rows:
    cols = row.find_all("td")

    if len(cols) >= 7:  
        date = cols[0].text.strip()  
        match_type = cols[1].text.strip()  
        round_number = cols[2].text.strip() if cols[2].text.strip() else "N/A"  
        teams = cols[3].text.strip().replace("\xa0", " ")   
        result = cols[4].text.strip() if cols[4].text.strip() else "Ej spelad" 
        venue = cols[5].text.strip()  
        attendance = cols[6].text.strip().replace(" ", "").replace("\xa0", "")  

        
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


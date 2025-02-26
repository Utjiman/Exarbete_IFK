import requests
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = "https://ifkdb.se/rekord"


response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")


records = []


record_rows = soup.select("p")  

for row in record_rows:
    text = row.text.strip()
    if text:
        
        parts = text.split(": ", 1)  
        if len(parts) == 2:
            category, value = parts
        else:
            category = parts[0]
            value = "N/A"

        
        records.append({"Kategori": category, "Värde": value})


df = pd.DataFrame(records)
df.to_csv("../data/raw/ifk_records_raw.csv", index=False)

print("✅ Skrapning klar! Sparade rekorddata till data/raw/ifk_records_raw.csv")

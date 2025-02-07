import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL till rekord-sidan
BASE_URL = "https://ifkdb.se/rekord"

# Skicka en request och hämta HTML
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

# Lista för att lagra rekorddata
records = []

# Hitta alla rader som innehåller rekord
record_rows = soup.select("p")  # Rekorden verkar ligga i <p>-taggar

for row in record_rows:
    text = row.text.strip()
    if text:
        # Dela upp rekord i kategori och värde
        parts = text.split(": ", 1)  # Delar vid första ": "
        if len(parts) == 2:
            category, value = parts
        else:
            category = parts[0]
            value = "N/A"

        # Lagra i listan
        records.append({"Kategori": category, "Värde": value})

# Konvertera till DataFrame och spara
df = pd.DataFrame(records)
df.to_csv("../data/raw/ifk_records_raw.csv", index=False)

print("✅ Skrapning klar! Sparade rekorddata till data/raw/ifk_records_raw.csv")

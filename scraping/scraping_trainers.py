import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL till tränarsidan
BASE_URL = "https://ifkdb.se/listor/allatranare"

# Skicka request och hämta HTML
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

# Lista för att lagra tränardata
coaches = []

# Hitta alla tränarblock
trainers = soup.select("div#inners div")

for trainer in trainers:
    # Hämta tränartitel (Huvudtränare / Interimtränare + år)
    title = trainer.find("span").text.strip() if trainer.find("span") else "Okänt"

    # Hämta tränarens namn
    name_tag = trainer.find("a")
    name = name_tag.text.strip() if name_tag else "Okänd"

    # Hämta tränarens matcher och säsonger
    details = trainer.find_all("span")[-1].text.strip() if trainer.find_all("span") else "Okänt"

    # Lagra tränaren i listan
    coaches.append({
        "Titel": title,
        "Namn": name,
        "Detaljer": details
    })

# Konvertera till DataFrame och spara till CSV
df = pd.DataFrame(coaches)
df.to_csv("../data/raw/ifk_coaches_raw.csv", index=False)

print("✅ Skrapning klar! Sparade tränardata till data/raw/ifk_coaches_raw.csv")

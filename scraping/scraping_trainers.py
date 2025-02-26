import requests
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = "https://ifkdb.se/listor/allatranare"


response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")


coaches = []


trainers = soup.select("div#inners div")

for trainer in trainers:
    
    title = trainer.find("span").text.strip() if trainer.find("span") else "Okänt"

    
    name_tag = trainer.find("a")
    name = name_tag.text.strip() if name_tag else "Okänd"

   
    details = trainer.find_all("span")[-1].text.strip() if trainer.find_all("span") else "Okänt"

    
    coaches.append({
        "Titel": title,
        "Namn": name,
        "Detaljer": details
    })


df = pd.DataFrame(coaches)
df.to_csv("../data/raw/ifk_coaches_raw.csv", index=False)

print("✅ Skrapning klar! Sparade tränardata till data/raw/ifk_coaches_raw.csv")

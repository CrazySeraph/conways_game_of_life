import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL der Top-100-Filme von IMDb
url = "https://www.imdb.com/chart/top/"

# HTTP-Anfrage an die IMDb-Website senden
response = requests.get(url)

# BeautifulSoup-Objekt aus dem HTML-Inhalt der Antwort erstellen
soup = BeautifulSoup(response.content, "html.parser")

# Alle Filmtitel, Bewertungen und Beschreibungen aus dem HTML-Inhalt extrahieren
titles = [title.text for title in soup.select("td.titleColumn a")]
ratings = [float(rating["data-value"]) for rating in soup.select("td.posterColumn span[name='ir']")]
descriptions = [description["title"] for description in soup.select("td.titleColumn span[title]")]

# Sicherstellen, dass alle Arrays die gleiche Länge haben
lengths = [len(titles), len(ratings), len(descriptions)]
if min(lengths) != max(lengths):
    min_length = min(lengths)
    titles = titles[:min_length]
    ratings = ratings[:min_length]
    descriptions = descriptions[:min_length]

# Pandas DataFrame mit den extrahierten Daten erstellen
data = pd.DataFrame({
    "Title": titles,
    "Rating": ratings,
    "Description": descriptions
})

# DataFrame anzeigen
print(data.head())
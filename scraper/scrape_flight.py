import requests
from bs4 import BeautifulSoup
import os

# URL til FIDS data
url = "https://fids.kefairport.is/site/apaops/?theme=%2Fthemes%2Fbootstrap.theme.darkly.min.css&sorts[arr_dep]=1&sorts[sched_time]=1&sorts[expected_time]=1&sorts[block_time]=1"

# Send forespørsel
response = requests.get(url)

# Sjekk at forespørselen var vellykket
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Hent alt innholdet fra siden
    full_content = soup.prettify()  # Tar hele HTML-strukturen

    # Generer HTML-fil med scraped data
    html_output = f"""
    <html>
    <head>
        <title>Full Page Content</title>
        <meta http-equiv="refresh" content="600">  <!-- Oppdater hver 10. minutt -->
    </head>
    <body>
        <h2>Full Page Text Content</h2>
        <pre>{full_content}</pre>  <!-- Vis hele innholdet i en preformateringsblokk -->
    </body>
    </html>
    """

    # Lagre filen
    os.makedirs("scraper/output", exist_ok=True)
    with open("scraper/output/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)

    print("Data har blitt skrevet til index.html i fulltekstformat!")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

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
    
    # Hent all tekst fra nettsiden som en enkel test
    all_text = soup.get_text()

    # Skriv ut til konsollen for testing
    print("All text from the page:")
    print(all_text)
    
    # Generer en enkel HTML-fil med all tekst fra siden
    html_output = f"""
    <html>
    <head>
        <title>Full Page Test</title>
        <meta http-equiv="refresh" content="600">  <!-- Oppdater hver 10. minutt -->
    </head>
    <body>
        <h2>Full Page Text Content</h2>
        <pre>{all_text}</pre>
    </body>
    </html>
    """

    # Opprett 'output'-mappen hvis den ikke finnes
    output_dir = "scraper/output"
    os.makedirs(output_dir, exist_ok=True)

    # Lagre test.html i output-mappen
    with open(f"{output_dir}/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)

    print("Data has been successfully written to index.html")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

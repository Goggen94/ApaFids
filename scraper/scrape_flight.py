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

    # Finn tabellen med flyinformasjon
    table = soup.find('table', {'class': 'table'})

    # Start å lage HTML-fil med scraped data
    html_output = """
    <html>
    <head>
        <title>Flight Information</title>
        <meta http-equiv="refresh" content="600">  <!-- Oppdater hver 10. minutt -->
        <style>
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 8px 12px; border: 1px solid black; text-align: left; }
            th { background-color: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h2>KEF Airport Flight Information</h2>
        <table>
            <tr>
                <th>Flight Number</th>
                <th>Destination</th>
                <th>Scheduled Time</th>
                <th>Expected Time</th>
                <th>Status</th>
                <th>Gate</th>
            </tr>
    """

    # Gå gjennom hver rad i tabellen
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) > 5:
            flight_number = cells[0].text.strip()
            destination = cells[2].text.strip()
            sched_time = cells[4].text.strip()
            expected_time = cells[5].text.strip()
            status = cells[7].text.strip()
            gate = cells[9].text.strip()

            html_output += f"""
            <tr>
                <td>{flight_number}</td>
                <td>{destination}</td>
                <td>{sched_time}</td>
                <td>{expected_time}</td>
                <td>{status}</td>
                <td>{gate}</td>
            </tr>
            """

    html_output += """
        </table>
    </body>
    </html>
    """

    # Lagre filen
    os.makedirs("scraper/output", exist_ok=True)
    with open("scraper/output/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)

    print("Flydata har blitt skrevet til index.html!")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

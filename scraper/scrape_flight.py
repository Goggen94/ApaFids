import requests
from bs4 import BeautifulSoup
import os
import json

# URL til FIDS data
url = "https://fids.kefairport.is/site/apaops/?theme=%2Fthemes%2Fbootstrap.theme.darkly.min.css&sorts[arr_dep]=1&sorts[sched_time]=1&sorts[expected_time]=1&sorts[block_time]=1"

# Send forespørsel
response = requests.get(url)

# Sjekk at forespørselen var vellykket
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finn tabellen med flyinformasjon
    table = soup.find('table', {'class': 'table'})
    
    # Hvis ingen tabell ble funnet
    if table is None:
        print("Fant ingen tabell på siden. Sjekk HTML-strukturen.")
        print(soup.prettify())  # Legger ut hele HTML-strukturen til loggen
    else:
        # Generer HTML-fil med scraped data
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
                    <th>Status</th>
                </tr>
        """

        flights_data = []
        # Gå gjennom rader og celler i tabellen
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) > 3:
                flight_number = cells[0].text.strip()
                destination = cells[1].text.strip()
                scheduled_time = cells[2].text.strip()
                status = cells[3].text.strip()

                flights_data.append({
                    "flight_number": flight_number,
                    "destination": destination,
                    "scheduled_time": scheduled_time,
                    "status": status
                })

                html_output += f"""
                <tr>
                    <td>{flight_number}</td>
                    <td>{destination}</td>
                    <td>{scheduled_time}</td>
                    <td>{status}</td>
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
        
        # Lagre JSON-data for testing
        with open("scraper/output/flight_data.json", "w", encoding="utf-8") as json_file:
            json.dump(flights_data, json_file, indent=4)

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

import requests
from bs4 import BeautifulSoup
import os

# URL to the flight data API
url = "https://fids.kefairport.is/api/flights?dateFrom=2024-10-08T13:37&dateTo=2024-10-09T02:37"

# Send the request to get the flight data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    
    # Generate HTML file with only departing flights
    html_output = """
    <html>
    <head>
        <title>KEF Departing Flights</title>
        <meta http-equiv="refresh" content="600">  <!-- Refresh every 10 minutes -->
        <style>
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 8px 12px; border: 1px solid black; text-align: left; }
            th { background-color: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h2>KEF Airport Departing Flights Information</h2>
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

    for flight in data:
        origin = flight.get("origin_iata", "")
        arr_dep = flight.get("arr_dep", "")
        
        # Filter to include only departing flights from KEF
        if origin == "KEF" and arr_dep == "Departing":
            flight_number = flight.get("flight_prefix", "") + flight.get("flight_num", "")
            destination = flight.get("destination", "N/A")
            sched_time = flight.get("sched_time", "N/A")
            expected_time = flight.get("expected_time", "N/A")
            status = flight.get("status", "N/A")
            gate = flight.get("gate", "N/A")
            
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

    # Save the HTML file to the output directory
    os.makedirs("scraper/output", exist_ok=True)
    with open("scraper/output/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

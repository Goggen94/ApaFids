import requests
from bs4 import BeautifulSoup
import os
import json

# API URL to get FIDS data
api_url = "https://fids.kefairport.is/api/flights?dateFrom=2024-10-08T13:37&dateTo=2024-10-09T02:37"

# Fetch the data from the API
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    flights_data = response.json()

    # Start creating the HTML content
    html_output = """
    <html>
    <head>
        <title>Flight Information</title>
        <meta http-equiv="refresh" content="600">  <!-- Refresh every 10 minutes -->
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
                <th>Origin</th>
                <th>Destination</th>
                <th>Scheduled Time</th>
                <th>Expected Time</th>
                <th>Status</th>
                <th>Gate</th>
            </tr>
    """

    # Iterate over the flight data and populate the table rows
    for flight in flights_data:
        flight_number = flight.get("flt", "N/A")
        origin = flight.get("origin", "N/A")
        destination = flight.get("destination", "N/A")
        scheduled_time = flight.get("sched_time", "N/A")
        expected_time = flight.get("expected_time", "N/A")
        status = flight.get("status", "N/A")
        gate = flight.get("gate", "N/A")

        # Add each flight row to the HTML table
        html_output += f"""
        <tr>
            <td>{flight_number}</td>
            <td>{origin}</td>
            <td>{destination}</td>
            <td>{scheduled_time}</td>
            <td>{expected_time}</td>
            <td>{status}</td>
            <td>{gate}</td>
        </tr>
        """

    # Close the table and HTML tags
    html_output += """
        </table>
    </body>
    </html>
    """

    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Write the HTML content to the index.html file
    with open("output/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)

    print("Flight data has been written to output/index.html")

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

import requests
import os
from datetime import datetime

# URL to the flight data API
url = "https://fids.kefairport.is/api/flights?dateFrom=2024-10-08T13:37&dateTo=2024-10-09T02:37"

# Send the request to get the flight data
response = requests.get(url)

# Function to format the time and date into separate columns
def format_time_and_date(time_str):
    try:
        # Parse the time string (expected format is "YYYY-MM-DDTHH:MM:SSZ")
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%H:%M"), dt.strftime("%d-%m")  # Return time (HH:MM) and date (DD-MM)
    except Exception as e:
        return "N/A", "N/A"  # If there's an issue, return N/A

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    
    # Generate HTML file with only departing flights excluding FI, LH, WK, and AY
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
        <h2>KEF Airport Departing Flights</h2>
        <table>
            <tr>
                <th>Flight Number</th>
                <th>Destination</th>
                <th>Scheduled Time</th>
                <th>Date</th>
                <th>Expected Time</th>
                <th>Date</th>
                <th>Status</th>
                <th>Gate</th>
            </tr>
    """

    excluded_airlines = ["FI", "LH", "WK", "AY"]

    for flight in data:
        destination = flight.get("destination_iata", "")
        flight_prefix = flight.get("flight_prefix", "")

        # Exclude flights with Keflavik (KEF) as destination and flights with specific prefixes
        if destination != "KEF" and flight_prefix not in excluded_airlines:
            flight_number = flight_prefix + flight.get("flight_num", "")
            destination_name = flight.get("destination", "N/A")
            sched_time, sched_date = format_time_and_date(flight.get("sched_time", "N/A"))
            expected_time, expected_date = format_time_and_date(flight.get("expected_time", "N/A"))
            status = flight.get("status", "N/A")
            gate = flight.get("gate", "N/A")
            
            html_output += f"""
                <tr>
                    <td>{flight_number}</td>
                    <td>{destination_name}</td>
                    <td>{sched_time}</td>
                    <td>{sched_date}</td>
                    <td>{expected_time}</td>
                    <td>{expected_date}</td>
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

    print("HTML file has been generated with formatted flight times.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

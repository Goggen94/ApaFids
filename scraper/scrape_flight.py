import requests
import os

# URL to the flight data API
url = "https://fids.kefairport.is/api/flights?dateFrom=2024-10-08T13:37&dateTo=2024-10-09T02:37"

# Send the request to get the flight data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data

    # Generate HTML file with only departing flights, excluding specified airline prefixes
    html_output = """
    <html>
    <head>
        <title>KEF Departing Flights (Excluding FI, LH, WK, AY)</title>
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
                <th>Expected Time</th>
                <th>Status</th>
                <th>Gate</th>
            </tr>
    """

    # Filter flights that are departing from KEF and exclude specified airline prefixes
    excluded_airlines = ('FI', 'LH', 'WK', 'AY')
    for flight in data:
        if flight['origin'] == 'KEF' and not flight['flight_prefix'].startswith(excluded_airlines):
            flight_number = flight.get('flight_prefix') + flight.get('flight_num')
            destination = flight.get('destination')
            sched_time = flight.get('sched_time', 'N/A')
            expected_time = flight.get('expected_time', 'N/A')
            status = flight.get('status', 'N/A')
            gate = flight.get('gate', 'N/A')

            # Add flight details to HTML output
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

    # Save the HTML output
    os.makedirs("output", exist_ok=True)
    with open("output/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")


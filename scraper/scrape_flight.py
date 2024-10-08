import requests
import os

# API URL to fetch flight data
url = "https://fids.kefairport.is/api/flights?dateFrom=2024-10-08T13:37&dateTo=2024-10-09T02:37"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Generate HTML content
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
                <th>Destination</th>
                <th>Scheduled Time</th>
                <th>Expected Time</th>
                <th>Status</th>
                <th>Gate</th>
            </tr>
    """

    # Loop through the flight data
    for flight in data:
        flight_number = flight.get('flight_prefix', '') + flight.get('flight_num', '')
        destination = flight.get('destination', '')
        sched_time = flight.get('sched_time', '')
        expected_time = flight.get('expected_time', '')
        status = flight.get('status', '')
        gate = flight.get('gate', '')

        # Add each flight's data to the table
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

    # Complete the HTML structure
    html_output += """
        </table>
    </body>
    </html>
    """

    # Save the result as an index.html in the output directory
    os.makedirs("output", exist_ok=True)
    with open("output/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

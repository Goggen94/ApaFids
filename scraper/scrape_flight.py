import requests
import os
from datetime import datetime, timedelta

# Function to get the current time and the time 24 hours ahead
def get_time_range():
    now = datetime.utcnow()  # Get the current UTC time
    date_from = now.strftime("%Y-%m-%dT%H:%M:%SZ")  # Format start time as "YYYY-MM-DDTHH:MM:SSZ"
    date_to = (now + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")  # 24 hours ahead
    return date_from, date_to

# Generate the time range for the API query
date_from, date_to = get_time_range()

# URL to the flight data API, dynamically adding the dateFrom and dateTo values
url = f"https://fids.kefairport.is/api/flights?dateFrom={date_from}&dateTo={date_to}"

# Send the request to get the flight data
response = requests.get(url)

# Function to format the time and date into separate columns
def format_time(time_str):
    try:
        # Parse the time string (expected format is "YYYY-MM-DDTHH:MM:SSZ")
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%H:%M")  # Return time (HH:MM)
    except Exception as e:
        return "N/A"  # If there's an issue, return N/A

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    
    # Generate HTML file with only departing flights handled by APA
    html_output = """
    <html>
    <head>
        <title>KEF Departing Flights (Handled by APA)</title>
        <meta http-equiv="refresh" content="600">  <!-- Refresh every 10 minutes -->
        <style>
            body {
                background-color: #2c2c2c;
                color: white;
                font-family: Arial, sans-serif;
            }
            h2 {
                text-align: center;
                color: #f4d03f;
                font-size: 24px;
                padding: 15px;
                border-radius: 8px;
                background-color: #444444;
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                margin: 20px auto;
                border-collapse: collapse;
                background-color: #333333;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #666666;
            }
            th {
                background-color: #f4d03f;
                color: #333;
                font-weight: bold;
                border-radius: 5px;
                font-size: 14px;
            }
            tr:nth-child(even) {
                background-color: #2c2c2c;
            }
            tr:hover {
                background-color: #444444;
            }
            td {
                color: #ddd;
            }
        </style>
    </head>
    <body>
        <h2>KEF Airport Departing Flights (Handled by APA)</h2>
        <table>
            <tr>
                <th>Flight</th>
                <th>Destination</th>
                <th>STD</th>
                <th>ETD</th>
                <th>Status</th>
                <th>Stand</th>
                <th>Gate</th>
            </tr>
    """

    for flight in data:
        destination = flight.get("destination_iata", "")
        handling_agent = flight.get("handling_agent", "")

        # Filter flights handled by APA and departing from KEF
        if destination != "KEF" and handling_agent == "APA":
            flight_number = flight.get("flight_prefix", "") + flight.get("flight_num", "")
            destination_name = flight.get("destination", "N/A")
            
            # Format scheduled and expected time
            sched_time = format_time(flight.get("sched_time", "N/A"))
            expected_time = format_time(flight.get("expected_time", "N/A"))
            
            status = flight.get("status", "N/A")
            stand = flight.get("stand", "N/A")
            gate = flight.get("gate", "N/A")
            
            html_output += f"""
                <tr>
                    <td>{flight_number}</td>
                    <td>{destination_name}</td>
                    <td>{sched_time}</td>
                    <td>{expected_time}</td>
                    <td>{status}</td>
                    <td>{stand}</td>
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

    print("HTML file has been generated with departing flights handled by APA.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

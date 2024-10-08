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
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%H:%M"), dt.date()  # Return time (HH:MM) and date
    except Exception as e:
        return "", None  # If there's an issue, return an empty string

# Function to calculate boarding-related times
def calculate_event_times(sched_time, flight_prefix):
    try:
        sched_dt = datetime.strptime(sched_time, "%Y-%m-%dT%H:%M:%SZ")
        if flight_prefix in ["W4", "W6", "W9"]:
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (sched_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")
        else:
            checkin_opens_time = (sched_dt - timedelta(hours=3)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(hours=1)).strftime("%H:%M")
            boarding_time = (sched_dt - timedelta(minutes=45)).strftime("%H:%M")
            final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (sched_dt - timedelta(minutes=20)).strftime("%H:%M")
            gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")
        return boarding_time, final_call_time, name_call_time, gate_closed_time, checkin_opens_time, checkin_closes_time
    except:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# Function to generate the tracking link using the aircraft registration
def generate_flightradar_link(aircraft_reg):
    if aircraft_reg:
        return f"https://www.flightradar24.com/{aircraft_reg}"  # Return the tracking URL
    else:
        return "#"  # Return a placeholder link if no aircraft registration

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    previous_date = None  # Track the date to insert the yellow line when the day changes

    # Generate HTML file with only departing flights handled by APA
    html_output = """
    <html>
    <head>
        <title>KEF Airport Departures</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="600">  <!-- Refresh every 10 minutes -->
        <style>
            body {
                background-color: #2c2c2c;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 16px;
            }
            h2 {
                text-align: center;
                color: #f4d03f;
                font-size: 24px;
                padding: 10px;
                border-radius: 8px;
                background-color: #444444;
                margin-bottom: 15px;
            }
            table {
                width: 100%;
                margin: 15px auto;
                border-collapse: collapse;
                background-color: #333333;
            }
            th, td {
                padding: 8px 12px;
                text-align: left;
                border-bottom: 1px solid #666666;
                font-weight: bold;
            }
            th {
                background-color: #f4d03f;
                color: #333;
                font-weight: bold;
                border-radius: 5px;
                font-size: 14px;
            }
            td {
                font-size: 14px;
            }
            tr:nth-child(even) {
                background-color: #2c2c2c;
            }
            tr:hover {
                background-color: #444444;
            }
            #next-day {
                background-color: #f4d03f;
                color: black;
                font-weight: bold;
                text-align: center;
                padding: 8px;
            }
            #popup {
                display: none;
                position: fixed;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                background-color: #444;
                padding: 8px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                z-index: 999;
                color: white;
                font-size: 16px;
                width: 40%;
            }
            #popup h3 {
                color: #f4d03f;
                font-size: 16px;
                margin-bottom: 5px;
            }
            #popup p {
                margin: 2px 0;
                font-size: 16px;
                display: flex;
                justify-content: space-between;
            }
            #close-popup {
                cursor: pointer;
                color: #f4d03f;
                margin-top: 8px;
                text-align: center;
                display: block;
            }
            a {
                color: #f4d03f;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
        <script>
            function showPopup(flight, boarding, finalCall, nameCall, gateClosed, checkinOpens, checkinCloses, flightradarLink) {
                document.getElementById("popup").style.display = "block";
                document.getElementById("flight-info").innerHTML = '<a href="' + flightradarLink + '" target="_blank">Flight: ' + flight + '</a>';
                document.getElementById("boarding").innerHTML = "Boarding: " + boarding;
                document.getElementById("final-call").innerHTML = "Final Call: " + finalCall;
                document.getElementById("name-call").innerHTML = "Name Call: " + nameCall;
                document.getElementById("gate-closed").innerHTML = "Gate Closed: " + gateClosed;
                document.getElementById("checkin-opens").innerHTML = "Check-in opens: " + checkinOpens;
                document.getElementById("checkin-closes").innerHTML = "Check-in closes: " + checkinCloses;
            }

            function closePopup() {
                document.getElementById("popup").style.display = "none";
            }
        </script>
    </head>
    <body>
        <h2>KEF Airport Departures</h2>
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
        flight_number = flight.get("flight_prefix", "") + flight.get("flight_num", "")
        status = flight.get("status", "N/A")

        # Filter flights handled by APA and exclude status "DYNAMIC MESSAGING"
        if destination != "KEF" and handling_agent == "APA" and status != "DYNAMIC MESSAGING":
            destination_name = flight.get("destination", "N/A")
            
            sched_time = flight.get("sched_time", "N/A")
            formatted_sched_time, sched_date = format_time(sched_time)
            expected_time = flight.get("expected_time", "")
            formatted_etd_time, _ = format_time(expected_time)
            time_for_popup = expected_time if expected_time != "" else sched_time

            # Apply popup logic for "OG", "W4", "W6", "W9" flights
            if flight_number.startswith(("OG", "W4", "W6", "W9")):
                boarding, final_call, name_call, gate_closed, checkin_opens, checkin_closes = calculate_event_times(sched_time, flight_number[:2])
                row_click = f"onclick=\"showPopup('{flight_number}', '{boarding}', '{final_call}', '{name_call}', '{gate_closed}', '{checkin_opens}', '{checkin_closes}', '#')\""
            else:
                row_click = ""

            stand = flight.get("stand", "N/A")
            gate = flight.get("gate", "N/A")

            if previous_date and sched_date != previous_date:
                html_output += f"""
                <tr id="next-day">
                    <td colspan="7">Next Day Flights</td>
                </tr>
                """
            
            html_output += f"""
                <tr {row_click}>
                    <td>{flight_number}</td>
                    <td>{destination_name}</td>
                    <td>{formatted_sched_time}</td>
                    <td>{formatted_etd_time}</td>
                    <td>{status}</td>
                    <td>{stand}</td>
                    <td>{gate}</td>
                </tr>
            """

            previous_date = sched_date

    html_output += """
        </table>

        <div id="popup">
            <h3>Flight Information</h3>
            <p id="flight-info">Flight:</p>
            <p id="boarding">Boarding:</p>
            <p id="final-call">Final Call:</p>
            <p id="name-call">Name Call:</p>
            <p id="gate-closed">Gate Closed:</p>
            <p id="checkin-opens">Check-in opens:</p>
            <p id="checkin-closes">Check-in closes:</p>
            <p id="close-popup" onclick="closePopup()">Close</p>
        </div>
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

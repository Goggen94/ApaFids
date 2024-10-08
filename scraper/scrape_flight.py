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
def calculate_event_times(sched_time):
    try:
        sched_dt = datetime.strptime(sched_time, "%Y-%m-%dT%H:%M:%SZ")
        go_to_gate_time = (sched_dt - timedelta(minutes=60)).strftime("%H:%M")
        boarding_time = (sched_dt - timedelta(minutes=45)).strftime("%H:%M")
        final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
        name_call_time = (sched_dt - timedelta(minutes=20)).strftime("%H:%M")
        gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")
        checkin_opens_time = (sched_dt - timedelta(hours=3)).strftime("%H:%M")  # Check-in opens 3 hours before STD
        checkin_closes_time = (sched_dt - timedelta(hours=1)).strftime("%H:%M")  # Check-in closes 1 hour before STD
        return go_to_gate_time, boarding_time, final_call_time, name_call_time, gate_closed_time, checkin_opens_time, checkin_closes_time
    except:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    previous_date = None  # Track the date to insert the yellow line when the day changes

    # Generate HTML file with only departing flights handled by APA
    html_output = """
    <html>
    <head>
        <title>KEF Departing Flights (Handled by APA)</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="600">  <!-- Refresh every 10 minutes -->
        <style>
            body {
                background-color: #2c2c2c;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 18px;
            }
            h2 {
                text-align: center;
                color: #f4d03f;
                font-size: 28px;
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
                padding: 10px 15px;
                text-align: left;
                border-bottom: 1px solid #666666;
                font-weight: bold;  /* Gjør teksten tykkere */
            }
            th {
                background-color: #f4d03f;
                color: #333;
                font-weight: bold;
                border-radius: 5px;
                font-size: 16px;
            }
            td {
                font-size: 16px;
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
                padding: 10px;
            }
            #popup {
                display: none;
                position: fixed;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                background-color: #444;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
                z-index: 999;
                color: white;
                font-size: 18px;
            }
            #popup h3 {
                color: #f4d03f;
            }
            #popup p {
                margin: 10px 0;
            }
            #popup .left {
                float: left;
                width: 50%;
                padding-right: 10px;
            }
            #popup .right {
                float: right;
                width: 50%;
                padding-left: 10px;
            }
            #close-popup {
                cursor: pointer;
                color: #f4d03f;
                margin-top: 10px;
                clear: both;
            }
            @media only screen and (max-width: 600px) {
                body {
                    font-size: 20px;
                }
                table {
                    width: 100%;
                }
                th, td {
                    font-size: 18px;
                    padding: 12px 10px;
                }
                h2 {
                    font-size: 24px;
                }
                #popup {
                    width: 90%;
                    padding: 15px;
                }
            }
        </style>
        <script>
            function showPopup(flight, goToGate, boarding, finalCall, nameCall, gateClosed, checkinOpens, checkinCloses) {
                document.getElementById("popup").style.display = "block";
                document.getElementById("flight-info").innerHTML = "Flight: " + flight;
                document.getElementById("go-to-gate").innerHTML = "Go to Gate: " + goToGate;
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
        flight_number = flight.get("flight_prefix", "") + flight.get("flight_num", "")

        # Filter flights handled by APA and departing from KEF, and limit popup to "OG" flights
        if destination != "KEF" and handling_agent == "APA":
            destination_name = flight.get("destination", "N/A")
            
            # Format scheduled and expected time
            sched_time = flight.get("sched_time", "N/A")
            formatted_sched_time, sched_date = format_time(sched_time)
            expected_time = flight.get("expected_time", "")
            formatted_etd_time, _ = format_time(expected_time)
            
            # Check if ETD exists, use it for the popup instead of STD if present
            time_for_popup = expected_time if expected_time != "" else sched_time

            # Calculate event times (only for OG flights)
            if flight_number.startswith("OG"):
                go_to_gate, boarding, final_call, name_call, gate_closed, checkin_opens, checkin_closes = calculate_event_times(time_for_popup)
                row_click = f"onclick=\"showPopup('{flight_number}', '{go_to_gate}', '{boarding}', '{final_call}', '{name_call}', '{gate_closed}', '{checkin_opens}', '{checkin_closes}')\""
            else:
                row_click = ""

            status = flight.get("status", "N/A")
            stand = flight.get("stand", "N/A")
            gate = flight.get("gate", "N/A")
            
            # Insert yellow line when the day changes
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

            previous_date = sched_date  # Update the previous_date for next iteration

    html_output += """
        </table>

        <div id="popup">
            <div class="left">
                <p id="checkin-opens"></p>
                <p id="checkin-closes"></p>
            </div>
            <div class="right">
                <h3>Additional Information</h3>
                <p id="flight-info"></p>
                <p id="go-to-gate"></p>
                <p id="boarding"></p>
                <p id="final-call"></p>
                <p id="name-call"></p>
                <p id="gate-closed"></p>
            </div>
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

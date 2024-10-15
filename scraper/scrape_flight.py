import requests
import os
from datetime import datetime, timedelta
import urllib3  # ADD THIS

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # ADD THIS

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

# Send the request to get the flight data (SSL verification disabled)
response = requests.get(url, verify=False)

# Function to format the time and date into separate columns
def format_time(time_str):
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%H:%M"), dt.date()  # Return time (HH:MM) and date
    except Exception as e:
        return "", None  # Return an empty string if there's an issue

# Function to calculate times related to check-in and gate events based on flight code
def calculate_event_times(sched_time, event_time_for_gate, flight_number):
    try:
        sched_dt = datetime.strptime(sched_time, "%Y-%m-%dT%H:%M:%SZ")
        event_dt = datetime.strptime(event_time_for_gate, "%Y-%m-%dT%H:%M:%SZ")

        # Default times based on the flight number
        checkin_opens_time, checkin_closes_time = "", ""
        go_to_gate_time, boarding_time, final_call_time, name_call_time, gate_closed_time = "", "", "", "", ""

        # Flight code-specific times
        if flight_number.startswith("OG"):
            checkin_opens_time = (sched_dt - timedelta(hours=3)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(hours=1)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith(("W4", "W6", "W9")):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            go_to_gate_time = (event_dt - timedelta(minutes=60)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith(("EZY", "EJU")):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            go_to_gate_time = (event_dt - timedelta(minutes=60)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=45)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("TOM"):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            go_to_gate_time = (event_dt - timedelta(minutes=60)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("BT"):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("BA"):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=45)).strftime("%H:%M")
            go_to_gate_time = (event_dt - timedelta(minutes=60)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=50)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith(("HV", "TO")):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("NO"):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("DL"):
            checkin_opens_time = (sched_dt - timedelta(hours=3, minutes=15)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(hours=1)).strftime("%H:%M")
            go_to_gate_time = (event_dt - timedelta(minutes=60)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=50)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=20)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("LS"):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("I2"):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("EW"):
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")

        # Return the calculated event times
        return go_to_gate_time, boarding_time, final_call_time, name_call_time, gate_closed_time, checkin_opens_time, checkin_closes_time

    except Exception as e:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# Sample HTML output generation
html_output = "<html><body><h1>Flight Data</h1></body></html>"

# Define the output directory for the generated HTML
output_dir = "scraper/output"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Now we write the HTML file
try:
    with open(f"{output_dir}/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)
    print(f"HTML file has been successfully saved to {output_dir}/index.html")
except Exception as e:
    print(f"Failed to write the HTML file: {e}")

# Create a Flightradar24 URL using aircraft_reg for OG flights, and flight number -1 for W4, W6, W9 flights
def generate_flightradar_link(flight_number, aircraft_reg):
    try:
        if flight_number.startswith("OG") and aircraft_reg and aircraft_reg != "N/A":
            return f"https://www.flightradar24.com/{aircraft_reg}"  # Use A/C Reg for OG flights
        elif flight_number.startswith(("W4", "W6", "W9")):
            flight_num = int(flight_number[2:]) - 1  # Subtract 1 from the flight number for W4, W6, W9
            return f"https://www.flightradar24.com/{flight_number[:2]}{flight_num}"
        elif flight_number.startswith(("EZY", "EJU")):
            flight_num = int(flight_number[3:]) - 1  # Use U2(flight number) - 1 for EZY and EJU
            return f"https://www.flightradar24.com/U2{flight_num}"
        else:
            return "#"
    except:
        return "#"  # Return a placeholder link if there's an error

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    previous_date = None  # Track the date to insert the yellow line when the day changes

    # Generate HTML file with only departing flights handled by APA
    html_output = f"""
    <html>
    <head>
        <title>KEF Airport Departures</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="60">  <!-- Refresh every minute -->
        <style>
            body {{ background-color: #2c2c2c; color: white; font-family: Arial, sans-serif; font-size: 16px; }}
            h2 {{ text-align: center; color: #f4d03f; font-size: 24px; padding: 10px; border-radius: 8px; background-color: #444444; margin-bottom: 15px; }}
            table {{ width: 100%; margin: 15px auto; border-collapse: collapse; background-color: #333333; }}
            th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #666666; font-weight: bold; }}
            th {{ background-color: #f4d03f; color: #333; font-weight: bold; border-radius: 5px; font-size: 14px; }}
            td {{ font-size: 14px; }}
            tr:nth-child(even) {{ background-color: #2c2c2c; }}
            tr:hover {{ background-color: #444444; }}
            #next-day {{ background-color: #f4d03f; color: black; font-weight: bold; text-align: center; padding: 8px; }}
            a {{ color: #f4d03f; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
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
                <th>Gate</th>
                <th>Flightradar24</th>
            </tr>
    """

    for flight in data:
        destination = flight.get("destination_iata", "")
        handling_agent = flight.get("handling_agent", "")
        flight_number = flight.get("flight_prefix", "") + flight.get("flight_num", "")
        status = flight.get("status", "N/A")
        etd_time = flight.get("expected_time", "")
        aircraft_reg = flight.get("aircraft_reg", "N/A")  # Get A/C Reg for OG flights

        # Remove N/A from ETD column
        formatted_etd_time, _ = format_time(etd_time) if etd_time != "" else ("", None)

        # Filter flights handled by APA and departing from KEF
        if destination != "KEF" and handling_agent == "APA":
            destination_name = flight.get("destination", "N/A")
            
            # Format scheduled time (STD)
            sched_time = flight.get("sched_time", "N/A")
            formatted_sched_time, sched_date = format_time(sched_time)

            # Use STD for Check-in Information and ETD for Gate Information if available
            gate_sched_time = etd_time if etd_time else sched_time

            # Calculate times for check-in and gate events
            go_to_gate, boarding, final_call, name_call, gate_closed, checkin_opens, checkin_closes = calculate_event_times(sched_time, gate_sched_time, flight_number)

            # Generate Flightradar link for W4, W6, W9 flights using flight number -1, and OG flights using A/C Reg
            flightradar_link = generate_flightradar_link(flight_number, aircraft_reg)

            row_click = f"onclick=\"showPopup('{flight_number}', '{go_to_gate}', '{boarding}', '{final_call}', '{name_call}', '{gate_closed}', '{checkin_opens}', '{checkin_closes}', '{flightradar_link}')\""

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
                    <td><a href="{flightradar_link}" target="_blank">Track</a></td>
                </tr>
            """

            previous_date = sched_date  # Update the previous_date for next iteration

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

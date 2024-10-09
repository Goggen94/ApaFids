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

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    data = None

# Function to format the time and date into separate columns
def format_time(time_str):
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%H:%M"), dt.date()  # Return time (HH:MM) and date
    except Exception as e:
        return "", None  # Return an empty string if there's an issue

# Function to calculate flight-specific event times based on flight code
def calculate_event_times_by_flight_code(flight_code, sched_time):
    try:
        sched_dt = datetime.strptime(sched_time, "%Y-%m-%dT%H:%M:%SZ")
        
        if flight_code in ["EZY", "EJU"]:
            # Check-in for EZY, EJU flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            go_to_gate_time = (sched_dt - timedelta(minutes=60)).strftime("%H:%M")
            boarding_time = (sched_dt - timedelta(minutes=45)).strftime("%H:%M")
            final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
            gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")
        
        elif flight_code in ["TO", "HV"]:
            # Check-in for TO, HV flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (sched_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")

        elif flight_code == "NO":
            # Check-in for NO flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (sched_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")

        elif flight_code == "LS":
            # Check-in for LS flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (sched_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")

        elif flight_code == "I2":
            # Check-in for I2 flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (sched_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")

        elif flight_code.startswith("OG"):
            # OG flights follow original logic with +1 on Flightradar link
            checkin_opens_time = (sched_dt - timedelta(hours=3)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(hours=1)).strftime("%H:%M")
            go_to_gate_time = (sched_dt - timedelta(minutes=60)).strftime("%H:%M")
            boarding_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (sched_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")

        elif flight_code.startswith(("W4", "W6", "W9")):
            # W flights use -1 for Flightradar URL
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            go_to_gate_time = (sched_dt - timedelta(minutes=60)).strftime("%H:%M")
            boarding_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (sched_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (sched_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (sched_dt - timedelta(minutes=15)).strftime("%H:%M")

        else:
            # No pop-up for unlisted flight codes
            return None, None, None, None, None, None, None

        return go_to_gate_time, boarding_time, final_call_time, name_call_time, gate_closed_time, checkin_opens_time, checkin_closes_time

    except:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# Create a Flightradar24 URL using aircraft_reg for OG flights, and flight number -1 for W4, W6, W9 flights
def generate_flightradar_link(flight_number, aircraft_reg):
    try:
        if flight_number.startswith("OG") and aircraft_reg and aircraft_reg != "N/A":
            return f"https://www.flightradar24.com/{aircraft_reg}"  # Use A/C Reg for OG flights
        else:
            flight_num = int(flight_number[2:]) - 1  # Subtract 1 from the flight number for W4, W6, W9
            return f"https://www.flightradar24.com/{flight_number[:2]}{flight_num}"
    except:
        return "#"  # Return a placeholder link if there's an error

# Ensure that data is not None before processing it
if data:
    for flight in data:
        destination = flight.get("destination_iata", "")
        handling_agent = flight.get("handling_agent", "")
        flight_number = flight.get("flight_prefix", "") + flight.get("flight_num", "")
        flight_code = flight.get("flight_prefix", "")

        # Skip flights that aren't in the desired list
        if flight_code not in ["EZY", "EJU", "TO", "HV", "NO", "LS", "I2", "OG", "W4", "W6", "W9"]:
            continue  # No pop-up for these flights

        sched_time = flight.get("sched_time", "N/A")
        go_to_gate, boarding, final_call, name_call, gate_closed, checkin_opens, checkin_closes = calculate_event_times_by_flight_code(flight_code, sched_time)

        # Generate Flightradar link for OG and W flights
        aircraft_reg = flight.get("aircraft_reg", "N/A")
        flightradar_link = generate_flightradar_link(flight_number, aircraft_reg)

        # Process the rest of your HTML and logic for displaying data
else:
    print("No data to process.")

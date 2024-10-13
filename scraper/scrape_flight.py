import requests
import os
from datetime import datetime, timedelta

# Function to get the current time and the time 24 hours ahead
def get_time_range():
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
            # OG flights
            checkin_opens_time = (sched_dt - timedelta(hours=3)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(hours=1)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith(("W4", "W6", "W9")):
            # W4, W6, W9 flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith(("EZY", "EJU")):
            # EZY, EJU flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            go_to_gate_time = (event_dt - timedelta(minutes=60)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=45)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith(("TO", "HV")):
            # TO, HV flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("NO"):
            # NO flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("LS"):
            # LS flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("I2"):
            # I2 flights
            checkin_opens_time = (sched_dt - timedelta(hours=2, minutes=30)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(minutes=40)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")
        elif flight_number.startswith("DL"):
            # DL flights
            checkin_opens_time = (sched_dt - timedelta(hours=3)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(hours=1)).strftime("%H:%M")
            go_to_gate_time = (event_dt - timedelta(minutes=60)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=50)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=20)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")

        return go_to_gate_time, boarding_time, final_call_time, name_call_time, gate_closed_time, checkin_opens_time, checkin_closes_time
    except Exception as e:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# Create a Flightradar24 URL using aircraft_reg for OG flights, and flight number -1 for W4, W6, W9 flights
def generate_flightradar_link(flight_number, aircraft_reg):
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
        <meta http-equiv="refresh" content="600">  <!-- Refresh every 10 minutes -->
        <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js"></script>
        <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging.js"></script>
        <script>
            const firebaseConfig = {{
                apiKey: "AIzaSyDebqZBQtfPbR6Nx84HnfN6qLX7LrLMWJY",
                authDomain: "paxbot-2b8b2.firebaseapp.com",
                projectId: "paxbot-2b8b2",
                storageBucket: "paxbot-2b8b2.appspot.com",
                messagingSenderId: "315115333501",
                appId: "1:315115333501:web:f9503954d0b067fb2ece14",
                measurementId: "G-S0Y63P27KG"
            }};
            
            // Initialize Firebase

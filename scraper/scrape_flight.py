import requests
import os
from datetime import datetime, timedelta
import json

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
        # Add more conditions as needed for other flight codes
        return go_to_gate_time, boarding_time, final_call_time, name_call_time, gate_closed_time, checkin_opens_time, checkin_closes_time
    except Exception as e:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# Generate the Flightradar24 link based on flight number or aircraft registration
def generate_flightradar_link(flight_number, aircraft_reg):
    try:
        if flight_number.startswith("OG") and aircraft_reg and aircraft_reg != "N/A":
            return f"https://www.flightradar24.com/{aircraft_reg}"
        else:
            flight_num = int(flight_number[2:]) - 1
            return f"https://www.flightradar24.com/{flight_number[:2]}{flight_num}"
    except:
        return "#"

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
            #popup {{ display: none; position: fixed; left: 50%; top: 50%; transform: translate(-50%, -50%); background-color: #444; padding: 8px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); z-index: 999; color: white; font-size: 16px; width: 40%; }}
            #popup h3 {{ color: #f4d03f; font-size: 16px; margin-bottom: 5px; }}
            #popup p {{ margin: 2px 0; font-size: 16px; }}
            #close-popup {{ cursor: pointer; color: #f4d03f; margin-top: 8px; text-align: center; display: block; }}
            a {{ color: #f4d03f; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            #last-updated {{ text-align: right; color: #f4d03f; font-size: 14px; padding-right: 20px; }}
            @media only screen and (max-width: 600px) {{
                #popup {{ width: 75%; padding: 8px; }}
            }}
        </style>

        <script src="https://www.gstatic.com/firebasejs/9.1.3/firebase-app.js"></script>
        <script src="https://www.gstatic.com/firebasejs/9.1.3/firebase-messaging.js"></script>
        <script>
          // Firebase-konfigurasjon
          const firebaseConfig = {{
            apiKey: "DIN_FIREBASE_API_KEY",
            authDomain: "DIN_FIREBASE_AUTH_DOMAIN",
            projectId: "DIN_FIREBASE_PROJECT_ID",
            storageBucket: "DIN_FIREBASE_STORAGE_BUCKET",
            messagingSenderId: "DIN_FIREBASE_MESSAGING_SENDER_ID",
            appId: "DIN_FIREBASE_APP_ID",
            measurementId: "DIN_FIREBASE_MEASUREMENT_ID"
          }};

          // Initialiser Firebase
          firebase.initializeApp(firebaseConfig);
          const messaging = firebase.messaging();

          // Registrer Service Worker
          if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/firebase-messaging-sw.js')
            .then(function(registration) {{
              console.log('Service Worker registration successful with scope: ', registration.scope);
            }}).catch(function(err) {{
              console.log('Service Worker registration failed: ', err);
            }});
          }}

          function requestNotificationPermission(flightNumber) {{
            messaging.requestPermission().then(function() {{
              console.log('Notification permission granted.');
              return messaging.getToken({{vapidKey: 'BORcM0w_fU1TmJDZAUbj5TeZLZdMGiJ0qfIIU1JeoN6fudf3ZV12S9g8bGGfr2dpwP2yKYtur5vKJsd9BfT2u10'}});
            }}).then(function(token) {{
              // Send token og flightNumber til backend
              subscribeToPush(token, flightNumber);
            }}).catch(function(err) {{
              console.log('Unable to get permission to notify.', err);
            }});
          }}

          function subscribeToPush(token, flightNumber) {{
            fetch('/subscribe', {{
              method: 'POST',
              headers: {{
                'Content-Type': 'application/json'
              }},
              body: JSON.stringify({{
                token: token,
                flight_number: flightNumber
              }})
            }});
          }}
        </script>
    </head>
    <body>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2>KEF Airport Departures</h2>
        </div>
        <div id="last-updated">Last updated: {datetime.now().strftime('%H:%M')}</div>
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
                    <td>{gate}</td>
                </tr>
            """

            previous_date = sched_date  # Update the previous_date for next iteration

    html_output += """
        </table>

        <div id="popup">
            <div class="info-container">
                <div>
                    <h3>Check-in Information</h3>
                    <p id="checkin-opens">Check-in opens:</p>
                    <p id="checkin-closes">Check-in closes:</p>
                </div>
                <div>
                    <h3>Gate Information</h3>
                    <p id="flight-info">Flight:</p>
                    <p id="go-to-gate">Go to Gate:</p>
                    <p id="boarding">Boarding:</p>
                    <p id="final-call">Final Call:</p>
                    <p id="name-call">Name Call:</p>
                    <p id="gate-closed">Gate Closed:</p>
                </div>
            </div>
            <button id="notify-btn">Notify me</button>
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
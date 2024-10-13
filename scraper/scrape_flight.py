import requests
import os
from datetime import datetime, timedelta

# Function to get the current time and the time 24 hours ahead
def get_time_range():
    now = datetime.utcnow()
    date_from = now.strftime('%Y-%m-%dT%H:%M:%SZ')  # Current time in UTC
    date_to = (now + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')  # 24 hours ahead
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

        # Example logic for specific flight codes
        if flight_number.startswith("OG"):
            checkin_opens_time = (sched_dt - timedelta(hours=3)).strftime("%H:%M")
            checkin_closes_time = (sched_dt - timedelta(hours=1)).strftime("%H:%M")
            boarding_time = (event_dt - timedelta(minutes=40)).strftime("%H:%M")
            final_call_time = (event_dt - timedelta(minutes=30)).strftime("%H:%M")
            name_call_time = (event_dt - timedelta(minutes=25)).strftime("%H:%M")
            gate_closed_time = (event_dt - timedelta(minutes=15)).strftime("%H:%M")

        return go_to_gate_time, boarding_time, final_call_time, name_call_time, gate_closed_time, checkin_opens_time, checkin_closes_time
    except Exception as e:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

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
            const app = firebase.initializeApp(firebaseConfig);
            const messaging = firebase.messaging();

            let currentETA = null;  // Store the current ETA globally
            let notify15minTimeout = null;  // Store the timeout ID for 15 min notification
            let notify5minTimeout = null;   // Store the timeout ID for 5 min notification

            messaging.requestPermission().then(() => {{
                console.log('Notification permission granted.');
                return messaging.getToken({{ vapidKey: '{os.getenv("VAPID_PUBLIC_KEY")}' }});
            }}).then((token) => {{
                console.log('Token:', token);
            }}).catch((err) => {{
                console.error('Error getting permission', err);
            }});

            messaging.onMessage((payload) => {{
                console.log('Message received', payload);
                alert('Flight Notification: ' + payload.notification.body);
            }});

            function notifyUser(flight) {{
                alert("You will be notified 15 minutes before and 5 minutes before flight " + flight + " lands!");
            }}

            function showPopup(flight, eta) {{
                document.getElementById("popup").style.display = "block";
                document.getElementById("flight-info").innerHTML = 'Flight: ' + flight;
                
                currentETA = new Date(eta);  // Set current ETA
                scheduleNotification(flight, currentETA);
                
                // Periodically check for ETA updates every 1 minute
                setInterval(function() {{
                    checkForUpdatedETA(flight);
                }}, 60000);  // Every 60 seconds
            }}

            function scheduleNotification(flight, eta) {
    const currentTime = new Date();
    const notify15minBefore = new Date(eta.getTime() - 15 * 60000);  // 15 minutes before
    const notify5minBefore = new Date(eta.getTime() - 5 * 60000);    // 5 minutes before

    const timeTo15min = notify15minBefore.getTime() - currentTime.getTime();
    const timeTo5min = notify5minBefore.getTime() - currentTime.getTime();

    // Clear any existing notifications
    if (notify15minTimeout) clearTimeout(notify15minTimeout);
    if (notify5minTimeout) clearTimeout(notify5minTimeout);

    // Schedule new notifications based on the updated ETA
    if (timeTo15min > 0) {
        notify15minTimeout = setTimeout(function() {
            alert("Flight " + flight + " will land in 15 minutes!");
        }, timeTo15min);
    }

    if (timeTo5min > 0) {
        notify5minTimeout = setTimeout(function() {
            alert("Flight " + flight + " will land in 5 minutes!");
        }, timeTo5min);
    }
}

            // Check for updated ETA and reschedule notifications if it changes
            function checkForUpdatedETA(flight) {{
                fetch(`/api/flights/${{flight}}`)  // You need to replace this with your actual API endpoint
                    .then(response => response.json())
                    .then(data => {{
                        const updatedETA = new Date(data.eta);  // Assume data.eta contains the updated ETA
                        if (updatedETA.getTime() !== currentETA.getTime()) {{
                            // ETA has changed, reschedule notifications
                            currentETA = updatedETA;  // Update the global ETA
                            scheduleNotification(flight, updatedETA);  // Reschedule notifications
                            console.log(`ETA updated for flight ${flight}: ${updatedETA}`);
                        }}
                    }})
                    .catch(error => {{
                        console.error('Error fetching updated ETA:', error);
                    }});
            }}

            function closePopup() {{
                document.getElementById("popup").style.display = "none";
            }}
        </script>
        <style>
            body {{ background-color: #2c2c2c; color: white; font-family: Arial, sans-serif; font-size: 16px; }}
            h2 {{ text-align: center; color: #f4d03f; font-size: 24px; padding: 10px; border-radius: 8px; background-color: #444444; margin-bottom: 15px; }}
            table {{ width: 100%; margin: 15px auto; border-collapse: collapse; background-color: #333333; }}
            th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #666666; font-weight: bold; }}
            th {{ background-color: #f4d03f; color: #333; font-weight: bold; border-radius: 5px; font-size: 14px; }}
            td {{ font-size: 14px; }}
            tr:nth-child(even) {{ background-color: #2c2c2c; }}
            tr:hover {{ background-color: #444444; }}
            #popup {{ display: none; position: fixed; left: 50%; top: 50%; transform: translate(-50%, -50%); background-color: #444; padding: 8px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); z-index: 999; color: white; font-size: 16px; width: 40%; }}
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
                <th>Stand</th>
                <th>Gate</th>
            </tr>
    """

    for flight in data:
        flight_number = flight.get("flight_prefix", "") + flight.get("flight_num", "")
        destination = flight.get("destination", "N/A")
        sched_time = flight.get("sched_time", "N/A")
        etd_time = flight.get("expected_time", "")
        eta_time = flight.get("eta", "")  # Extract the ETA time

        formatted_sched_time, _ = format_time(sched_time)
        formatted_etd_time, _ = format_time(etd_time)
        formatted_eta_time, _ = format_time(eta_time)  # Format ETA for display

        row_click = f"onclick=\"showPopup('{flight_number}', '{eta_time}')\""

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
                <td>{destination}</td>
                <td>{formatted_sched_time}</td>
                <td>{formatted_etd_time}</td>
                <td>{status}</td>
                <td>{stand}</td>
                <td>{gate}</td>
            </tr>
        """

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
            <button onclick="notifyUser(document.getElementById('flight-info').textContent)">Notify me</button>
            <p id="close-popup" onclick="closePopup()">Close</p>
        </div>

        <script>
            function showPopup(flight, goToGate, boarding, finalCall, nameCall, gateClosed, checkinOpens, checkinCloses, flightradarLink) {{
                document.getElementById("popup").style.display = "block";
                document.getElementById("flight-info").innerHTML = 'Flight: ' + flight;
                document.getElementById("go-to-gate").innerHTML = "Go to Gate: " + goToGate;
                document.getElementById("boarding").innerHTML = "Boarding: " + boarding;
                document.getElementById("final-call").innerHTML = "Final Call: " + finalCall;
                document.getElementById("name-call").innerHTML = "Name Call: " + nameCall;
                document.getElementById("gate-closed").innerHTML = "Gate Closed: " + gateClosed;
                document.getElementById("checkin-opens").innerHTML = "Check-in opens: " + checkinOpens;
                document.getElementById("checkin-closes").innerHTML = "Check-in closes: " + checkinCloses;
            }}

            function closePopup() {{
                document.getElementById("popup").style.display = "none";
            }}

            function notifyUser(flight) {{
                alert("You will be notified 15 minutes before and 5 minutes before flight " + flight + " lands!");
            }}
        </script>
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


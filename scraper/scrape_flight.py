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
        return "", None  # Return an empty string if there's an issue

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    previous_date = None  # Track the date to insert the yellow line when the day changes

    # Generate HTML file with arriving flights
    html_output = """
    <html>
    <head>
        <title>KEF Airport Departures</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="600">  <!-- Refresh every 10 minutes -->
        <style>
            body { background-color: #2c2c2c; color: white; font-family: Arial, sans-serif; font-size: 16px; }
            h2 { text-align: center; color: #f4d03f; font-size: 24px; padding: 10px; border-radius: 8px; background-color: #444444; margin-bottom: 15px; }
            table { width: 100%; margin: 15px auto; border-collapse: collapse; background-color: #333333; }
            th, td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #666666; font-weight: bold; }
            th { background-color: #f4d03f; color: #333; font-weight: bold; border-radius: 5px; font-size: 14px; }
            td { font-size: 14px; }
            tr:nth-child(even) { background-color: #2c2c2c; }
            tr:hover { background-color: #444444; }
            #next-day { background-color: #f4d03f; color: black; font-weight: bold; text-align: center; padding: 8px; }
            #popup { display: none; position: fixed; left: 50%; top: 50%; transform: translate(-50%, -50%); background-color: #444; padding: 8px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); z-index: 999; color: white; font-size: 16px; width: 40%;  /* Reduced size */ }
            #popup h3 { color: #f4d03f; font-size: 16px; margin-bottom: 5px; }
            #popup p { margin: 2px 0; font-size: 16px; display: flex; justify-content: space-between;  /* Vertical alignment */ }
            #close-popup { cursor: pointer; color: #f4d03f; margin-top: 8px; text-align: center; display: block; }
            a { color: #f4d03f;  /* Set link color to yellow */ text-decoration: none; }
            a:hover { text-decoration: underline; }
            #arrivals-btn {
                margin-top: 10px;
                padding: 6px 12px;
                background-color: #444444;
                color: #f4d03f;
                font-weight: bold;
                border-radius: 8px;
                text-decoration: none;
                border: 2px solid #f4d03f;
                cursor: pointer;
            }
            #last-updated {
                text-align: right;
                color: #f4d03f;
                font-size: 14px;
                padding-right: 20px;
            }
            @media only screen and (max-width: 600px) {
                #arrivals-btn {
                    margin-left: 20px;
                    margin-bottom: 20px;
                    display: block;
                }
                #arrivals-btn, #last-updated {
                    text-align: center;
                }
            }
        </style>
        <script>
            function showPopup(flight, flightradarLink) {
                document.getElementById("popup").style.display = "block";
                document.getElementById("flight-info").innerHTML = '<a href="' + flightradarLink + '" target="_blank">Flight: ' + flight + '</a>';
            }

            function closePopup() {
                document.getElementById("popup").style.display = "none";
            }
        </script>
    </head>
    <body>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2>KEF Airport Departures</h2>
            <a href="https://arr.paxnotes.com" id="arrivals-btn">Arrivals</a>
        </div>
        <div id="last-updated">Last updated: """ + datetime.now().strftime("%H:%M") + """</div>
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

            stand = flight.get("stand", "N/A")
            gate = flight.get("gate", "N/A")

            html_output += f"""
                <tr onclick="showPopup('{flight_number}', '#')">
                    <td>{flight_number}</td>
                    <td>{destination_name}</td>
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
            <h3>Flight Information</h3>
            <p id="flight-info">Flight:</p>
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

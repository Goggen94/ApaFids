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

# Modify the part of the code where flight pop-up times are calculated

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

    # Create the pop-up and continue with the rest of the logic

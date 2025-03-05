from initial_info import flights

def landed_flights():
    for flight in flights:
        flight_id = flight["flightId"]
        print(f"Flight {flight_id} has landed")

landed_flights()
from datetime import datetime

flights = [
    {
        "flightId": "FL-2025-001",
        "plateNumber": "EC-XYZ1",
        "arrivalTime": "2025-03-01T09:30:00",
        "departureTime": "2025-03-01T14:45:00",
        "fuelConsumption": 350,
        "occupiedSeats": 7,
        "origin": "Valencia",
        "destination": "Paris",
        "passengerIds": [("P-1001", 'Boarded'), ("P-1002", 'Boarded'), ("P-1003", 'Boarded'), ("P-1004", 'Boarded'), ("P-1005", 'Boarded'), ("P-1006", 'Boarded')]
    },
    {
        "flightId": "FL-2025-002",
        "plateNumber": "EC-ABC2",
        "arrivalTime": "2025-03-02T11:15:00",
        "departureTime": "2025-03-02T16:30:00",
        "fuelConsumption": 850,
        "occupiedSeats": 8,
        "origin": "Barcelona",
        "destination": "London",
        "passengerIds": [("P-1010", 'Boarded'), ("P-1011", 'Boarded'), ("P-1012", 'Cancelled'), ("P-1013", 'Boarded'), ("P-1014", 'Boarded'), ("P-1015", 'Boarded'), ("P-1016", 'Boarded'), ("P-1017", 'Cancelled')]
    }
]

def get_landed_flights(flights, reference_time=None):
    """
    Retrieve a list of flights that have already landed.
    
    :param flights: List of flight dictionaries
    :param reference_time: Optional datetime to use instead of current time for testing
    :return: List of landed flights
    """
    # Use provided reference time or current time
    current_time = reference_time if reference_time else datetime.now()
    
    landed_flights = []
    
    for flight in flights:
        arrival_time = datetime.fromisoformat(flight['arrivalTime'])
        
        if arrival_time <= current_time:
            landed_flight_info = {
                'Flight ID': flight['flightId'],
                'Plate Number': flight['plateNumber'],
                'Origin': flight['origin'],
                'Destination': flight['destination'],
                'Arrival Time': flight['arrivalTime'],
                'Occupied Seats': flight['occupiedSeats']
            }
            landed_flights.append(landed_flight_info)
    
    return landed_flights

def display_landed_flights(landed_flights):
    """
    Display detailed information about landed flights.
    
    :param landed_flights: List of landed flight dictionaries
    """
    if not landed_flights:
        print("No flights have landed yet.")
        return
    
    print("Landed Flights:")
    print("-" * 80)
    for flight in landed_flights:
        print(f"Flight ID: {flight['Flight ID']}")
        print(f"Aircraft: {flight['Plate Number']}")
        print(f"Route: {flight['Origin']} → {flight['Destination']}")
        print(f"Arrival Time: {flight['Arrival Time']}")
        print(f"Passengers Onboard: {flight['Occupied Seats']}")
        print("-" * 80)

def main():
    landed_flights = get_landed_flights(flights)
    display_landed_flights(landed_flights)

if __name__ == "__main__":
    main()
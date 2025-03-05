from datetime import datetime

# Flight data
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

# Passenger data
passengers = [
    {
        "passengerId": "P-1001",
        "name": "Ana García Martínez",
        "nationalId": "12345678A",
        "dateOfBirth": "1991-05-15",
    },
    {
        "passengerId": "P-1002",
        "name": "Carlos Rodríguez López",
        "nationalId": "87654321B",
        "dateOfBirth": "1973-11-30",
    },
    {
        "passengerId": "P-1003",
        "name": "Elena Sánchez García",
        "nationalId": "11223344C",
        "dateOfBirth": "1988-03-25",
    },
    {
        "passengerId": "P-1004",
        "name": "Javier Martínez Pérez",
        "nationalId": "44332211D",
        "dateOfBirth": "1995-07-10",
    },
    {
        "passengerId": "P-1005",
        "name": "María López Rodríguez",
        "nationalId": "33441122E",
        "dateOfBirth": "1985-09-05",
    },
    {
        "passengerId": "P-1006",
        "name": "Pedro García Sánchez",
        "nationalId": "22114433F",
        "dateOfBirth": "1979-01-20",
    },
    {
        "passengerId": "P-1010",
        "name": "Antonio García López",
        "nationalId": "88776655J",
        "dateOfBirth": "1980-06-05",
    },
    {
        "passengerId": "P-1011",
        "name": "Beatriz López Sánchez",
        "nationalId": "99887766K",
        "dateOfBirth": "1983-04-30",
    },
    {
        "passengerId": "P-1013",
        "name": "David Sánchez Martínez",
        "nationalId": "22110033M",
        "dateOfBirth": "1987-03-20",
    },
    {
        "passengerId": "P-1014",
        "name": "Elena García López",
        "nationalId": "33221100N",
        "dateOfBirth": "1978-07-25",
    },
    {
        "passengerId": "P-1015",
        "name": "Fernando López Martínez",
        "nationalId": "44332211O",
        "dateOfBirth": "1982-01-10",
    },
    {
        "passengerId": "P-1016",
        "name": "Gloria Martínez Sánchez",
        "nationalId": "55443322P",
        "dateOfBirth": "1984-09-05",
    }
]

def get_arrived_passengers(flights, passengers, reference_time=None):
    """
    Retrieve a list of passengers who have arrived at the aerodrome.
    
    :param flights: List of flight dictionaries
    :param passengers: List of passenger dictionaries
    :param reference_time: Optional datetime to use instead of current time for testing
    :return: List of arrived passengers with flight details
    """
    # Use provided reference time or current time
    current_time = reference_time if reference_time else datetime.now()
    
    arrived_passengers = []
    
    for flight in flights:
        arrival_time = datetime.fromisoformat(flight['arrivalTime'])
        
        # Check if flight has landed
        if arrival_time <= current_time:
            # Get boarded passengers for this flight
            boarded_passengers = [
                passenger_id for passenger_id, status in flight['passengerIds'] 
                if status == 'Boarded'
            ]
            
            # Find full passenger details
            for passenger_id in boarded_passengers:
                passenger_info = next(
                    (p for p in passengers if p['passengerId'] == passenger_id), 
                    None
                )
                
                if passenger_info:
                    arrived_passenger = {
                        'Passenger ID': passenger_info['passengerId'],
                        'Name': passenger_info['name'],
                        'National ID': passenger_info['nationalId'],
                        'Date of Birth': passenger_info['dateOfBirth'],
                        'Flight ID': flight['flightId'],
                        'Origin': flight['origin'],
                        'Arrival Time': flight['arrivalTime']
                    }
                    arrived_passengers.append(arrived_passenger)
    
    return arrived_passengers

def display_arrived_passengers(arrived_passengers):
    """
    Display detailed information about arrived passengers.
    
    :param arrived_passengers: List of arrived passenger dictionaries
    """
    if not arrived_passengers:
        print("No passengers have arrived yet.")
        return
    
    print("Arrived Passengers:")
    print("=" * 70)
    
    for passenger in arrived_passengers:
        print(f"Name: {passenger['Name']}")
        print(f"Passenger ID: {passenger['Passenger ID']}")
        print(f"National ID: {passenger['National ID']}")
        print(f"Date of Birth: {passenger['Date of Birth']}")
        print(f"Flight ID: {passenger['Flight ID']}")
        print(f"Origin: {passenger['Origin']}")
        print(f"Arrival Time: {passenger['Arrival Time']}")
        print("-" * 70)

def main():
    # For testing purposes, you can simulate different times
    # Uncomment and modify the line below to test with a specific reference time
    # reference_time = datetime.fromisoformat("2025-03-02T12:00:00")
    
    # Get arrived passengers
    arrived_passengers = get_arrived_passengers(flights, passengers)
    
    # Display arrived passengers
    display_arrived_passengers(arrived_passengers)

if __name__ == "__main__":
    main()
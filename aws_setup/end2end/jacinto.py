from initial_info import airplanes, flights, passengers

def display_airplanes():
    print("\n--- Airplanes in Hangar ---")
    for plane in airplanes:
        print(f"Plate: {plane['plateNumber']} | Type: {plane['type']} | Hangar: {plane['hangarId']} | Last maintenance: {plane['lastMaintenanceDate']}")

def display_flights():
    print("\n--- Landed Flights ---")
    for flight in flights:
        print(f"Flight ID: {flight['flightId']}")
        print(f"  Plane (Plate): {flight['plateNumber']}")
        print(f"  Route: {flight['origin']} -> {flight['destination']}")
        print(f"  Arrival: {flight['arrivalTime']} | Departure: {flight['departureTime']}")
        print(f"  Fuel consumption: {flight['fuelConsumption']} | Occupied seats: {flight['occupiedSeats']}")
        print("  Passengers:")
        for passenger_id, status in flight['passengerIds']:
            print(f"    {passenger_id} - Status: {status}")
        print()

def display_arrived_passengers():
    print("\n--- Arrived Passengers ---")
    # Recopilamos los IDs de pasajeros que tienen estado 'Boarded'
    boarded_ids = {pid for flight in flights for pid, status in flight['passengerIds'] if status.lower() == 'boarded'}
    # Filtramos la lista de pasajeros según los IDs recopilados
    arrived = [p for p in passengers if p['passengerId'] in boarded_ids]
    
    if arrived:
        for p in arrived:
            print(f"ID: {p['passengerId']} | Name: {p['name']} | DNI: {p['nationalId']} | DOB: {p['dateOfBirth']}")
    else:
        print("No arrived passengers found with status 'Boarded'.")

def run_app():
    while True:
        print("\n=== Aerodrome Management ===")
        print("1. Show airplanes in hangar")
        print("2. Show landed flights")
        print("3. Show arrived passengers")
        print("4. Exit")
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            display_airplanes()
        elif choice == '2':
            display_flights()
        elif choice == '3':
            display_arrived_passengers()
        elif choice == '4':
            print("Exiting the application...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == '__main__':
    run_app()

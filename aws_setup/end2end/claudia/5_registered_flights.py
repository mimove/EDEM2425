from initial_info import flights

def register_landed_flight(flight_id):
    for flight in flights:
        if flight["flightId"] == flight_id:
            print(f"The flight {flight['flightId']} with plate number {flight['plateNumber']} has landed from {flight['origin']} at {flight['arrivalTime']}.")
            return
    print("Flight not found.")

flight_number = input("Enter flight ID: ")
register_landed_flight(flight_number)

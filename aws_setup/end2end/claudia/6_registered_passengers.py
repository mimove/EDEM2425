from initial_info import passengers

def register_passenger(passenger_id):
    for passenger in passengers:
        if passenger["passengerId"] == passenger_id:
            print(f"The passenger with ID {passenger['passengerId']} is {passenger['name']}.")
            return
    print("Passenger not found.")

passenger_id = input("Enter passenger ID: ")
register_passenger(passenger_id)

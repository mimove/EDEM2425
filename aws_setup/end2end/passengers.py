from initial_info import passengers

def arrived_passengers():
    for passenger in passengers:
        name = passenger["name"]
        id = passenger["passengerId"]
        print(f"Passenger: {name} with ID {id} has arrived safely")

arrived_passengers()
        


from initial_info import airplanes, passengers, flights

def register_airplane():
    new_airplane = {
        "plateNumber": input('Introduce plate number: '),
        "type": input('Introduce the type of the airplane: '),
        "lastMaintenanceDate": input('Intruduce the last maintenance date: '),
        "nextMaintenanceDate": input('Intruduce the next maintenance date: '),
        "capacity": input('Intruduce the capacity: '),
        "ownerId": input('Introduce the owner ID: '),
        "ownerName": input("Introduce the owner name: "),
        "hangarId": input('Introduce the hangar ID: '),
        "fuel_capacity": input('Introduce the fuel capacity: ')
    }
    airplanes.append(new_airplane)
    print('Airplane registered:', new_airplane)
    return new_airplane

#### WIP
def register_flight():
    new_flight = {
        "flightId": input('Introduce flight ID: '),
        "plateNumber": input('Introduce the plate number: '),
        # "arrivalTime": input('Intruduce the arrival time: '),
        # "departureTime": input(),
        "fuelConsumption": input('Intruduce the fuel consumption: '),
        "occupiedSeats": input('Introduce the occupied seats: '),
        "origin": input('Introduce the origin of the flight: '),
        "destination": input('Introduce the destination of the flight: ')
        # "passengersIds": 
    }
    flights.append(new_flight)
    print('Airplane registered:', new_flight)
    return new_flight


def registration():
    register_new = input("Select register information (airplanes, flights or passengers): ").lower()
    if airplanes:
        register_airplane()
    elif flights:
        register_flight()
    else:
        print("Please, introduce a valid option")

registration()
from initial_info import airplanes, passengers, flights
from datetime import datetime


def get_airplanes():
    return airplanes 

def get_flights():
    return flights 

def get_passagers():
    return passengers

def _print_message(flight):
    print(f"Flight ID: {flight['flightId']}")
    print(f"Departure Time: {flight['departureTime']}")
    print(f"Arrival Time: {flight['arrivalTime']}")
    print(f"Origin: {flight['origin']}")
    print(f"Destination: {flight['destination']}")
    print(f"Plate Number: {flight['plateNumber']}")
    print(f"Fuel Consumption: {flight['fuelConsumption']}")
    print(f"Passenger IDs: {flight['passengerIds']}")
    print()

def detail_airplanes(airplanes):
    print("Airplanes Jacinto, vuela seguro")
    print(f"Numero de aviones disponibles en estos momentos en el hangar: {len(airplanes)}")
    print('''
-------------------
AIRPLANES JACINTO 
-------------------
''')
    
    for airplane in airplanes:
        print(f"Airplane numero {airplanes.index(airplane) +1}")
        print(f"Plate Number: {airplane['plateNumber']}")


def detail_flights(flights):
    print("Airplanes Jacinto, vuela seguro")
    time_now = datetime.now().replace(microsecond=0)  
    for flight in flights:
        departure_time = datetime.strptime(flight['departureTime'], "%Y-%m-%dT%H:%M:%S")
        arrival_time = datetime.strptime(flight['arrivalTime'], "%Y-%m-%dT%H:%M:%S")
        if departure_time <= time_now:
            print('''
--------------------------------
Vuelos han llegado llegar
--------------------------------
                  ''')
        else:
            print('''
--------------------------------
Vuelos por llegar
--------------------------------
                  ''')
        _print_message(flight)



if __name__ == '__main__':

    detail_airplanes(airplanes)

    detail_flights(flights)

    print('''
-----------------
A Fecha de:
          ''')
    print(datetime.now())

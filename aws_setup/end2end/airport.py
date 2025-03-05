import importlib.util
from datetime import datetime

file_path = "initial_info.py"
spec = importlib.util.spec_from_file_location("initial_info", file_path)
initial_info = importlib.util.module_from_spec(spec)
spec.loader.exec_module(initial_info)

flights = initial_info.flights
airplanes = initial_info.airplanes
passengers = initial_info.passengers

landed_planes = {flight["plateNumber"] for flight in flights}

planes_in_hangars = set()
current_time = datetime.now().isoformat()

for airplane in airplanes:
    plate_number = airplane["plateNumber"]
    has_future_flight = any(
        flight["plateNumber"] == plate_number and flight["departureTime"] > current_time
        for flight in flights
    )
    if not has_future_flight:
        planes_in_hangars.add(plate_number)

arrived_passengers = set()
for flight in flights:
    if flight["plateNumber"] in landed_planes:
        for passenger_id, status in flight["passengerIds"]:
            if status == "Boarded":
                arrived_passengers.add(passenger_id)

passenger_dict = {p["passengerId"]: p["name"] for p in passengers}

print("Aviones que han aterrizado:")
for airplane in airplanes:
    if airplane["plateNumber"] in landed_planes:
        print(f"- {airplane['plateNumber']} ({airplane['type']}) - {airplane['ownerName']}")

print("\nAviones en los hangares:")
for airplane in airplanes:
    if airplane["plateNumber"] in planes_in_hangars:
        print(f"- {airplane['plateNumber']} ({airplane['type']}) - {airplane['ownerName']} (Hangar: {airplane['hangarId']})")

print("\nPasajeros que han llegado al aeródromo:")
for passenger_id in arrived_passengers:
    print(f"- {passenger_dict.get(passenger_id, 'Desconocido')} (ID: {passenger_id})")

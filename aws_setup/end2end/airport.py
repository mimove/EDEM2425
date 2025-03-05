import importlib.util
import json
from datetime import datetime

# Cargar el archivo initial_info.py
file_path = "initial_info.py"
spec = importlib.util.spec_from_file_location("initial_info", file_path)
initial_info = importlib.util.module_from_spec(spec)
spec.loader.exec_module(initial_info)

# Extraer datos
flights = initial_info.flights
airplanes = initial_info.airplanes
passengers = initial_info.passengers

# Obtener aviones que han aterrizado
landed_planes = {flight["plateNumber"] for flight in flights}

# Obtener aviones que están en el hangar (sin vuelos futuros)
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

# Obtener pasajeros que han llegado al aeródromo
arrived_passengers = set()
for flight in flights:
    if flight["plateNumber"] in landed_planes:
        for passenger_id, status in flight["passengerIds"]:
            if status == "Boarded":
                arrived_passengers.add(passenger_id)

# Mapear IDs de pasajeros con sus nombres
passenger_dict = {p["passengerId"]: p["name"] for p in passengers}

# Mostrar aviones aterrizados
print("Aviones que han aterrizado:")
for airplane in airplanes:
    if airplane["plateNumber"] in landed_planes:
        print(f"- {airplane['plateNumber']} ({airplane['type']}) - {airplane['ownerName']}")

# Mostrar aviones en el hangar
print("\nAviones en los hangares:")
for airplane in airplanes:
    if airplane["plateNumber"] in planes_in_hangars:
        print(f"- {airplane['plateNumber']} ({airplane['type']}) - {airplane['ownerName']} (Hangar: {airplane['hangarId']})")

# Mostrar pasajeros que han llegado
print("\nPasajeros que han llegado al aeródromo:")
for passenger_id in arrived_passengers:
    print(f"- {passenger_dict.get(passenger_id, 'Desconocido')} (ID: {passenger_id})")


# ---------------------- REGISTRAR NUEVO AVIÓN ---------------------- #

def register_new_airplane():
    """Permite registrar un nuevo avión en el hangar o actualizar uno existente."""
    print("\nRegistrar un nuevo avión en el hangar:")

    plate_number = input("Matrícula del avión: ").strip().upper()
    
    # Verificar si el avión ya está registrado
    existing_airplane = next((a for a in airplanes if a["plateNumber"] == plate_number), None)

    if existing_airplane:
        print(f"El avión con matrícula {plate_number} ya está registrado. Se actualizará la información.")
    else:
        # Pedir datos del nuevo avión
        airplane_type = input("Tipo de avión: ").strip()
        owner_name = input("Nombre del propietario: ").strip()
        hangar_id = input("ID del hangar: ").strip().upper()
        fuel_capacity = int(input("Capacidad de combustible: ").strip())

        new_airplane = {
            "plateNumber": plate_number,
            "type": airplane_type,
            "lastMaintenanceDate": datetime.now().strftime("%Y-%m-%d"),
            "nextMaintenanceDate": (datetime.now().replace(year=datetime.now().year + 1)).strftime("%Y-%m-%d"),
            "capacity": int(input("Capacidad de pasajeros: ").strip()),
            "ownerId": f"O-{hash(owner_name) % 100000}",
            "ownerName": owner_name,
            "hangarId": hangar_id,
            "fuel_capacity": fuel_capacity
        }

        airplanes.append(new_airplane)
        print(f"✅ Nuevo avión {plate_number} registrado con éxito.")

    # Guardar cambios en el archivo
    save_data_to_file()


# ---------------------- REGISTRAR NUEVO VUELO ---------------------- #

def register_new_flight():
    """Permite registrar un nuevo vuelo aterrizado y agregarlo al historial."""
    print("\nRegistrar un nuevo vuelo aterrizado:")

    flight_id = input("ID del vuelo: ").strip().upper()
    plate_number = input("Matrícula del avión: ").strip().upper()
    arrival_time = input("Hora de llegada (YYYY-MM-DDTHH:MM:SS): ").strip()
    departure_time = input("Hora de salida (YYYY-MM-DDTHH:MM:SS): ").strip()
    fuel_consumption = int(input("Consumo de combustible: ").strip())
    occupied_seats = int(input("Número de pasajeros a bordo: ").strip())
    origin = input("Ciudad de origen: ").strip()
    destination = input("Ciudad de destino: ").strip()

    passenger_ids = []
    for _ in range(occupied_seats):
        passenger_id = input("ID del pasajero: ").strip().upper()
        passenger_status = "Boarded"
        passenger_ids.append((passenger_id, passenger_status))

    new_flight = {
        "flightId": flight_id,
        "plateNumber": plate_number,
        "arrivalTime": arrival_time,
        "departureTime": departure_time,
        "fuelConsumption": fuel_consumption,
        "occupiedSeats": occupied_seats,
        "origin": origin,
        "destination": destination,
        "passengerIds": passenger_ids
    }

    flights.append(new_flight)
    print(f"✅ Nuevo vuelo {flight_id} registrado con éxito.")

    # Guardar cambios en el archivo
    save_data_to_file()


# ---------------------- REGISTRAR NUEVO PASAJERO ---------------------- #

def register_new_passenger():
    """Permite registrar un nuevo pasajero en la base de datos."""
    print("\nRegistrar un nuevo pasajero en el aeródromo:")

    passenger_id = input("ID del pasajero: ").strip().upper()

    # Verificar si el pasajero ya existe
    existing_passenger = next((p for p in passengers if p["passengerId"] == passenger_id), None)

    if existing_passenger:
        print(f"El pasajero con ID {passenger_id} ya está registrado.")
    else:
        name = input("Nombre completo: ").strip()
        national_id = input("DNI/NIE/Pasaporte: ").strip().upper()
        date_of_birth = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()

        new_passenger = {
            "passengerId": passenger_id,
            "name": name,
            "nationalId": national_id,
            "dateOfBirth": date_of_birth
        }

        passengers.append(new_passenger)
        print(f"✅ Pasajero {name} registrado con éxito.")

    # Guardar cambios en el archivo
    save_data_to_file()


def save_data_to_file():
    """Guarda la lista actualizada de aviones, vuelos y pasajeros en initial_info.py."""
    with open("initial_info.py", "w", encoding="utf-8") as f:
        f.write("# Updated Data\n")
        f.write(f"airplanes = {json.dumps(airplanes, indent=4)}\n")
        f.write(f"flights = {json.dumps(flights, indent=4)}\n")
        f.write(f"passengers = {json.dumps(passengers, indent=4)}\n")
    
    print("✅ Registro actualizado en 'initial_info.py'.")


# Preguntar al usuario si desea registrar un nuevo avión, vuelo o pasajero
if input("\n¿Quieres registrar un nuevo avión en el hangar? (s/n): ").strip().lower() == "s":
    register_new_airplane()

if input("\n¿Quieres registrar un nuevo vuelo aterrizado? (s/n): ").strip().lower() == "s":
    register_new_flight()

if input("\n¿Quieres registrar un nuevo pasajero? (s/n): ").strip().lower() == "s":
    register_new_passenger()

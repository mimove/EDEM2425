from initial_info import airplanes, passengers, flights
from datetime import datetime
import json

def print_separator(char="-", length=60):
    print(char * length)

def print_header(title):
    print_separator("=")
    print(f"{title.center(60)}")
    print_separator("=")
    print()  # Línea en blanco para separar secciones

def print_table_header(columns, widths):
    """Imprime el encabezado de una tabla dado una lista de columnas y anchos"""
    header = "| " + " | ".join(f"{col:<{width}}" for col, width in zip(columns, widths)) + " |"
    print(header)
    print_separator()

def print_table_row(row, widths):
    """Imprime una fila de tabla dado una lista de valores y anchos"""
    print("| " + " | ".join(f"{str(value):<{width}}" for value, width in zip(row, widths)) + " |")

# Función para mostrar la información actualizada
def mostrar_informacion():
    current_time = datetime.now()

def registrar_avion():
    print("\nIntroduce los datos del nuevo avión:")
    plate_number = input("Matrícula: ")
    tipo = input("Tipo: ")
    last_maintenance = input("Fecha de último mantenimiento (YYYY-MM-DD): ")
    next_maintenance = input("Fecha de próximo mantenimiento (YYYY-MM-DD): ")
    capacity = int(input("Capacidad: "))
    owner_id = input("ID del propietario: ")
    owner_name = input("Nombre del propietario: ")
    hangar_id = input("ID del hangar: ")
    fuel_capacity = int(input("Capacidad de combustible: "))
    
    nuevo_avion = {
        "plateNumber": plate_number,
        "type": tipo,
        "lastMaintenanceDate": last_maintenance,
        "nextMaintenanceDate": next_maintenance,
        "capacity": capacity,
        "ownerId": owner_id,
        "ownerName": owner_name,
        "hangarId": hangar_id,
        "fuel_capacity": fuel_capacity
    }
    return nuevo_avion

def registrar_vuelo():
    print("\nIntroduce los datos del nuevo vuelo (ya aterrizado):")
    flight_id = input("ID del vuelo: ")
    plate_number = input("Matrícula del avión: ")
    origin = input("Origen: ")
    destination = input("Destino: ")
    departure_time = input("Hora de salida (YYYY-MM-DDTHH:MM:SS): ")
    arrival_time = input("Hora de llegada (YYYY-MM-DDTHH:MM:SS): ")
    fuel_consumption = int(input("Consumo de combustible: "))
    occupied_seats = int(input("Asientos ocupados: "))
    
    # Registro de pasajeros para el vuelo
    passenger_ids = []
    agregar = input("¿Desea registrar pasajeros para este vuelo? (s/n): ")
    while agregar.strip().lower() == "s":
        pid = input("ID del pasajero: ")
        estado = input("Estado (Boarded/Cancelled): ")
        passenger_ids.append((pid, estado))
        agregar = input("¿Agregar otro pasajero? (s/n): ")
    
    nuevo_vuelo = {
        "flightId": flight_id,
        "plateNumber": plate_number,
        "origin": origin,
        "destination": destination,
        "departureTime": departure_time,
        "arrivalTime": arrival_time,
        "fuelConsumption": fuel_consumption,
        "occupiedSeats": occupied_seats,
        "passengerIds": passenger_ids
    }
    return nuevo_vuelo

def mostrar_informacion():
    current_time = datetime.now()

    # 1. Mostrar la lista de vuelos que han aterrizado
    landed_flights = []
    for flight in flights:
        arrival = datetime.fromisoformat(flight["arrivalTime"])
        if arrival <= current_time:
            landed_flights.append(flight)

    print_header("VUELOS QUE HAN ATERRIZADO")
    if landed_flights:
        for flight in landed_flights:
            print(f"Flight ID       : {flight['flightId']}")
            print(f"Matrícula       : {flight['plateNumber']}")
            print(f"Origen/Destino  : {flight['origin']} -> {flight['destination']}")
            print(f"Hora salida     : {flight['departureTime']}")
            print(f"Hora llegada    : {flight['arrivalTime']}")
            print_separator()
            print()
    else:
        print("No hay vuelos aterrizados en este momento.")
        print()
    
    # 2. Avisar de vuelos con pasajeros cancelados, mostrando ID y nombre
    passenger_map = {p["passengerId"]: p["name"] for p in passengers}
    print_header("AVISOS DE VUELOS CON CANCELACIONES")
    found_cancelled = False
    for flight in flights:
        cancelled = [
            (pid, passenger_map.get(pid, "Nombre no encontrado"))
            for pid, status in flight["passengerIds"]
            if status.lower() == "cancelled"
        ]
        if cancelled:
            print(f"¡AVISO! El vuelo {flight['flightId']} tiene cancelaciones:")
            for pid, name in cancelled:
                print(f"    - {pid}: {name}")
            print_separator()
            print()
            found_cancelled = True
    if not found_cancelled:
        print("No hay avisos de cancelaciones en vuelos.")
        print()
    
    # 3. Mostrar aviones en el hangar y su estado, según los vuelos asignados
    print_header("ESTADO DE AVIONES")
    print(f"| {'Matrícula':<12} | {'Tipo':<25} | {'Estado':<20} |")
    print_separator()
    for airplane in airplanes:
        associated_flights = [flight for flight in flights if flight["plateNumber"] == airplane["plateNumber"]]
        status = "En hangar"
        if associated_flights:
            in_flight = False
            pending = False
            landed = False
            for flight in associated_flights:
                departure = datetime.fromisoformat(flight["departureTime"])
                arrival = datetime.fromisoformat(flight["arrivalTime"])
                if departure <= current_time < arrival:
                    in_flight = True
                    break
                elif current_time < departure:
                    pending = True
                elif current_time >= arrival:
                    landed = True
            if in_flight:
                status = "En vuelo"
            elif pending:
                status = "Pendiente de vuelo"
            elif landed:
                status = "Aterrizado y en hangar"
        print(f"| {airplane['plateNumber']:<12} | {airplane['type']:<25} | {status:<20} |")
    print_separator()
    print()
    
    # 4. Mostrar el estado de los pasajeros (ID y nombre) para cada vuelo
    print_header("ESTADO DE PASAJEROS POR VUELO")
    for flight in flights:
        print_separator()
        print(f"Para el vuelo {flight['flightId']}:")
        print(f"| {'ID Pasajero':<12} | {'Nombre':<30} | {'Estado':<10} |")
        print_separator()
        for pid, pstatus in flight["passengerIds"]:
            pname = passenger_map.get(pid, "Nombre no encontrado")
            print(f"| {pid:<12} | {pname:<30} | {pstatus:<10} |")
        print_separator()
        print()

# ---------------------------------------------------------------------------
# Registro interactivo de nuevos aviones
print_header("REGISTRO DE NUEVOS AVIONES")
seguir_avion = True
while seguir_avion:
    nuevo_avion = registrar_avion()
    airplanes.append(nuevo_avion)
    opcion = input("¿Desea registrar otro avión? (s/n): ")
    if opcion.strip().lower() != "s":
        seguir_avion = False

# Registro interactivo de nuevos vuelos (que ya han aterrizado)
print_header("REGISTRO DE NUEVOS VUELOS (YA ATERRIZADOS)")
seguir_vuelo = True
while seguir_vuelo:
    nuevo_vuelo = registrar_vuelo()
    flights.append(nuevo_vuelo)
    opcion = input("¿Desea registrar otro vuelo? (s/n): ")
    if opcion.strip().lower() != "s":
        seguir_vuelo = False

# Mostrar la información actualizada
print_header("INFORMACIÓN ACTUALIZADA")
mostrar_informacion()

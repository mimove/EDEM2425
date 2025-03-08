
from initial_info import airplanes, flights, passengers

def listar_vuelos():
    print("--- LISTA DE VUELOS ---")
    for vuelo in flights:
        print(f"ID de Vuelo: {vuelo['flightId']}")
        print(f"Número de Matrícula: {vuelo['plateNumber']}")
        print(f"Origen: {vuelo['origin']}")
        print(f"Destino: {vuelo['destination']}")
        print(f"Hora de Salida: {vuelo['departureTime']}")
        print(f"Hora de Llegada: {vuelo['arrivalTime']}")
        print(f"Asientos Ocupados: {vuelo['occupiedSeats']}")
        print(f"Consumo de Combustible: {vuelo['fuelConsumption']} litros")
        
        print("Pasajeros:")
        for pasajero_id, estado in vuelo['passengerIds']:
            pasajero = next((p for p in passengers if p['passengerId'] == pasajero_id), None)
            if pasajero:
                print(f"  - {pasajero['name']} (ID: {pasajero_id}, Estado: {estado})")
        print("\n")

def listar_aviones_en_hangares():
    print("--- AVIONES EN HANGARES ---")
    hangares = {}
    for avion in airplanes:
        hangar_id = avion['hangarId']
        if hangar_id not in hangares:
            hangares[hangar_id] = []
        hangares[hangar_id].append(avion)
    
    for hangar, aviones in hangares.items():
        print(f"Hangar: {hangar}")
        for avion in aviones:
            print(f"  - Matrícula: {avion['plateNumber']}")
            print(f"    Tipo: {avion['type']}")
            print(f"    Capacidad: {avion['capacity']} pasajeros")
            print(f"    Último mantenimiento: {avion['lastMaintenanceDate']}")
            print(f"    Próximo mantenimiento: {avion['nextMaintenanceDate']}")
            print(f"    Propietario: {avion['ownerName']}")
        print("\n")

def listar_pasajeros():
    print("--- LISTA DE PASAJEROS ---")
    for pasajero in passengers:
        print(f"ID: {pasajero['passengerId']}")
        print(f"Nombre: {pasajero['name']}")
        print(f"DNI: {pasajero['nationalId']}")
        print(f"Fecha de Nacimiento: {pasajero['dateOfBirth']}")
        print("\n")

if __name__ == "__main__":
    listar_vuelos()
    listar_aviones_en_hangares()
    listar_pasajeros()
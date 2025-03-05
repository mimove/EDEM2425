from initial_info import airplanes, flights, passengers

def list_airplanes():
    print("\n--- Lista de Aviones en Hangar ---")
    for plane in airplanes:
        print(f"Placa: {plane['plateNumber']}, Tipo: {plane['type']}, Hangares: {plane['hangarId']}, Último mantenimiento: {plane['lastMaintenanceDate']}")
        
def list_flights():
    print("\n--- Lista de Vuelos Aterrizados ---")
    for flight in flights:
        print(f"ID Vuelo: {flight['flightId']}")
        print(f"  Avión (Placa): {flight['plateNumber']}")
        print(f"  Origen: {flight['origin']}  ->  Destino: {flight['destination']}")
        print(f"  Hora de llegada: {flight['arrivalTime']}")
        print(f"  Hora de salida: {flight['departureTime']}")
        print(f"  Consumo de combustible: {flight['fuelConsumption']}")
        print(f"  Asientos ocupados: {flight['occupiedSeats']}")
        print("  Pasajeros:")
        for p in flight['passengerIds']:
            print(f"    ID: {p[0]}, Estado: {p[1]}")
        print()
        
def list_arrived_passengers():
    print("\n--- Lista de Pasajeros Llegados ---")
    # Recorremos todos los vuelos y obtenemos los pasajeros con estado 'Boarded'
    arrived_ids = set()
    for flight in flights:
        for pid, status in flight['passengerIds']:
            if status.lower() == 'boarded':
                arrived_ids.add(pid)
    # Buscamos la información del pasajero según el ID
    arrived_passengers = [p for p in passengers if p['passengerId'] in arrived_ids]
    
    if arrived_passengers:
        for p in arrived_passengers:
            print(f"ID: {p['passengerId']} - Nombre: {p['name']}, DNI: {p['nationalId']}, Fecha de nacimiento: {p['dateOfBirth']}")
    else:
        print("No se encontraron pasajeros con estado 'Boarded'.")

def main():
    while True:
        print("\n=== Gestión del Aeródromo ===")
        print("1. Ver lista de aviones en hangar")
        print("2. Ver lista de vuelos aterrizados")
        print("3. Ver lista de pasajeros que han llegado")
        print("4. Salir")
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            list_airplanes()
        elif opcion == '2':
            list_flights()
        elif opcion == '3':
            list_arrived_passengers()
        elif opcion == '4':
            print("Saliendo de la aplicación...")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == '__main__':
    main()

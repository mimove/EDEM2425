#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

# Datos extraídos del archivo paste.txt
airplanes = [
    {
        "plateNumber": "EC-XYZ1",
        "type": "Cessna 208 Caravan",
        "lastMaintenanceDate": "2024-04-15",
        "nextMaintenanceDate": "2025-04-15",
        "capacity": 9,
        "ownerId": "O-12345",
        "ownerName": "Madrid Flying Club",
        "hangarId": "H-01",
        "fuel_capacity": 700
    },
    {
        "plateNumber": "EC-ABC2",
        "type": "Piper PA-31 Navajo",
        "lastMaintenanceDate": "2025-02-10",
        "nextMaintenanceDate": "2027-02-10",
        "capacity": 7,
        "ownerId": "O-23456",
        "ownerName": "Catalina Aviation",
        "hangarId": "H-01",
        "fuel_capacity": 1000
    }
]

flights = [
    {
        "flightId": "FL-2025-001",
        "plateNumber": "EC-XYZ1",
        "arrivalTime": "2025-03-01T09:30:00",
        "departureTime": "2025-03-01T14:45:00",
        "fuelConsumption": 350,
        "occupiedSeats": 7,
        "origin": "Valencia",
        "destination": "Paris",
        "passengerIds": [("P-1001", 'Boarded'), ("P-1002", 'Boarded'), ("P-1003", 'Boarded'), 
                         ("P-1004", 'Boarded'), ("P-1005", 'Boarded'), ("P-1006", 'Boarded')]
    },
    {
        "flightId": "FL-2025-002",
        "plateNumber": "EC-ABC2",
        "arrivalTime": "2025-03-02T11:15:00",
        "departureTime": "2025-03-02T16:30:00",
        "fuelConsumption": 850,
        "occupiedSeats": 8,
        "origin": "Barcelona",
        "destination": "London",
        "passengerIds": [("P-1010", 'Boarded'), ("P-1011", 'Boarded'), ("P-1012", 'Cancelled'), 
                         ("P-1013", 'Boarded'), ("P-1014", 'Boarded'), ("P-1015", 'Boarded'), 
                         ("P-1016", 'Boarded'), ("P-1017", 'Cancelled')]
    }
]

passengers = [
    # Datos de pasajeros omitidos para mayor claridad
    # Se pueden incluir si son necesarios para la tarea
]

def get_airplane_details(plate_number):
    """Obtener detalles del avión por número de matrícula"""
    for airplane in airplanes:
        if airplane["plateNumber"] == plate_number:
            return airplane
    return None

def get_landed_flights(current_time=None):
    """
    Obtener lista de vuelos que ya han aterrizado
    
    Args:
        current_time (datetime, optional): Tiempo actual para comparar.
                                           Si es None, se usa el tiempo actual del sistema.
    
    Returns:
        list: Lista de vuelos aterrizados con detalles adicionales
    """
    if current_time is None:
        current_time = datetime.now()
    
    landed_flights = []
    
    for flight in flights:
        arrival_time = datetime.fromisoformat(flight["arrivalTime"])
        
        # Si la hora de llegada es anterior a la hora actual, el vuelo ha aterrizado
        if arrival_time < current_time:
            # Obtener información adicional del avión
            airplane = get_airplane_details(flight["plateNumber"])
            
            # Contar pasajeros abordados (excluyendo cancelados)
            boarded_passengers = sum(1 for _, status in flight["passengerIds"] if status == 'Boarded')
            
            # Agregar detalles del vuelo aterrizado
            landed_flight_info = {
                "flightId": flight["flightId"],
                "plateNumber": flight["plateNumber"],
                "aircraftType": airplane["type"] if airplane else "Unknown",
                "origin": flight["origin"],
                "arrivalTime": flight["arrivalTime"],
                "boardedPassengers": boarded_passengers,
                "ownerName": airplane["ownerName"] if airplane else "Unknown"
            }
            
            landed_flights.append(landed_flight_info)
    
    return landed_flights

def display_landed_flights():
    """Mostrar la información de vuelos aterrizados de manera formateada"""
    # Para propósitos de prueba, configuramos una fecha futura para ver todos los vuelos
    # En producción, se usaría datetime.now()
    test_current_time = datetime.fromisoformat("2025-03-03T00:00:00")
    
    landed_flights = get_landed_flights(test_current_time)
    
    if not landed_flights:
        print("No hay vuelos aterrizados hasta el momento.")
        return
    
    print("\n===================== VUELOS ATERRIZADOS =====================")
    print(f"Fecha de consulta: {test_current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("================================================================")
    
    for idx, flight in enumerate(landed_flights, 1):
        arrival_time = datetime.fromisoformat(flight["arrivalTime"])
        
        print(f"\n{idx}. VUELO: {flight['flightId']}")
        print(f"   Aeronave: {flight['plateNumber']} ({flight['aircraftType']})")
        print(f"   Operador: {flight['ownerName']}")
        print(f"   Origen: {flight['origin']}")
        print(f"   Llegada: {arrival_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Pasajeros a bordo: {flight['boardedPassengers']}")
    
    print("\n================================================================")
    print(f"Total de vuelos aterrizados: {len(landed_flights)}")
    print("================================================================\n")

if __name__ == "__main__":
    display_landed_flights()
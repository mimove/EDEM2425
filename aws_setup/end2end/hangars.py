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

def is_airplane_in_flight(plate_number, current_time=None):
    """
    Determinar si un avión está actualmente en vuelo
    
    Args:
        plate_number (str): Número de matrícula del avión
        current_time (datetime, optional): Tiempo actual para comparar.
                                          Si es None, se usa el tiempo actual del sistema.
    
    Returns:
        bool: True si el avión está en vuelo, False en caso contrario
    """
    if current_time is None:
        current_time = datetime.now()
    
    for flight in flights:
        if flight["plateNumber"] == plate_number:
            arrival_time = datetime.fromisoformat(flight["arrivalTime"])
            departure_time = datetime.fromisoformat(flight["departureTime"])
            
            # Si el tiempo actual está entre la llegada y la salida, o después de la salida pero antes de la llegada del próximo vuelo
            if arrival_time <= current_time <= departure_time:
                return False  # El avión está en el aeródromo entre vuelos
            elif current_time < arrival_time or current_time > departure_time:
                # Verificar si hay otro vuelo programado después
                for next_flight in flights:
                    if (next_flight["plateNumber"] == plate_number and 
                        datetime.fromisoformat(next_flight["arrivalTime"]) > departure_time and
                        datetime.fromisoformat(next_flight["arrivalTime"]) <= current_time):
                        return False  # El avión ya regresó de este vuelo
                
                # Si estamos después del tiempo de salida y no hay vuelos posteriores que hayan llegado
                if current_time > departure_time:
                    return True  # El avión está en vuelo
    
    # Si no hay vuelos programados para este avión, se considera que está en el hangar
    return False

def get_airplanes_in_hangars(current_time=None):
    """
    Obtener lista de aviones que están actualmente en los hangares
    
    Args:
        current_time (datetime, optional): Tiempo actual para comparar.
                                           Si es None, se usa el tiempo actual del sistema.
    
    Returns:
        list: Lista de aviones en hangares con detalles adicionales
    """
    if current_time is None:
        current_time = datetime.now()
    
    airplanes_in_hangars = []
    
    for airplane in airplanes:
        # Comprobar si el avión no está en vuelo (está en el hangar)
        if not is_airplane_in_flight(airplane["plateNumber"], current_time):
            # Verificar el próximo vuelo programado
            next_flight = None
            next_flight_time = None
            
            for flight in flights:
                if flight["plateNumber"] == airplane["plateNumber"]:
                    departure_time = datetime.fromisoformat(flight["departureTime"])
                    if departure_time > current_time:
                        if next_flight_time is None or departure_time < next_flight_time:
                            next_flight = flight
                            next_flight_time = departure_time
            
            # Agregar detalles del avión
            airplane_info = {
                "plateNumber": airplane["plateNumber"],
                "type": airplane["type"],
                "hangarId": airplane["hangarId"],
                "ownerName": airplane["ownerName"],
                "capacity": airplane["capacity"],
                "fuelCapacity": airplane["fuel_capacity"],
                "lastMaintenanceDate": airplane["lastMaintenanceDate"],
                "nextMaintenanceDate": airplane["nextMaintenanceDate"],
                "nextFlight": {
                    "flightId": next_flight["flightId"] if next_flight else None,
                    "departureTime": next_flight["departureTime"] if next_flight else None,
                    "destination": next_flight["destination"] if next_flight else None
                } if next_flight else None
            }
            
            airplanes_in_hangars.append(airplane_info)
    
    return airplanes_in_hangars

def display_airplanes_in_hangars():
    """Mostrar la información de aviones en hangares de manera formateada"""
    # Para propósitos de prueba, configuramos una fecha específica
    # En producción, se usaría datetime.now()
    test_current_time = datetime.fromisoformat("2025-03-01T12:00:00")
    
    airplanes_in_hangars = get_airplanes_in_hangars(test_current_time)
    
    if not airplanes_in_hangars:
        print("No hay aviones en los hangares en este momento.")
        return
    
    print("\n===================== AVIONES EN HANGARES =====================")
    print(f"Fecha de consulta: {test_current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=================================================================")
    
    hangars = {}
    # Agrupar aviones por hangar
    for airplane in airplanes_in_hangars:
        hangar_id = airplane["hangarId"]
        if hangar_id not in hangars:
            hangars[hangar_id] = []
        hangars[hangar_id].append(airplane)
    
    for hangar_id, hangar_airplanes in hangars.items():
        print(f"\nHangar: {hangar_id}")
        print("------------------------------------------------------------------")
        
        for idx, airplane in enumerate(hangar_airplanes, 1):
            print(f"\n{idx}. Aeronave: {airplane['plateNumber']} ({airplane['type']})")
            print(f"   Operador: {airplane['ownerName']}")
            print(f"   Capacidad: {airplane['capacity']} pasajeros | Combustible: {airplane['fuelCapacity']} unidades")
            print(f"   Último mantenimiento: {airplane['lastMaintenanceDate']} | Próximo: {airplane['nextMaintenanceDate']}")
            
            if airplane["nextFlight"]:
                next_departure = datetime.fromisoformat(airplane["nextFlight"]["departureTime"])
                print(f"   Próximo vuelo: {airplane['nextFlight']['flightId']} a {airplane['nextFlight']['destination']}")
                print(f"   Hora de salida: {next_departure.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print("   Próximo vuelo: No programado")
    
    print("\n=================================================================")
    print(f"Total de aviones en hangares: {len(airplanes_in_hangars)}")
    print("=================================================================\n")

if __name__ == "__main__":
    display_airplanes_in_hangars()
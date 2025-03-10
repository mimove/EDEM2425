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
    {
        "passengerId": "P-1001",
        "name": "Ana García Martínez",
        "nationalId": "12345678A",
        "dateOfBirth": "1991-05-15",
    },
    {
        "passengerId": "P-1002",
        "name": "Carlos Rodríguez López",
        "nationalId": "87654321B",
        "dateOfBirth": "1973-11-30",
    },
    {
        "passengerId": "P-1003",
        "name": "Elena Sánchez García",
        "nationalId": "11223344C",
        "dateOfBirth": "1988-03-25",
    },
    {
        "passengerId": "P-1004",
        "name": "Javier Martínez Pérez",
        "nationalId": "44332211D",
        "dateOfBirth": "1995-07-10",
    },
    {
        "passengerId": "P-1005",
        "name": "María López Rodríguez",
        "nationalId": "33441122E",
        "dateOfBirth": "1985-09-05",
    },
    {
        "passengerId": "P-1006",
        "name": "Pedro García Sánchez",
        "nationalId": "22114433F",
        "dateOfBirth": "1979-01-20",
    },
    {
        "passengerId": "P-1007",
        "name": "Sara Pérez Martínez",
        "nationalId": "55443322G",
        "dateOfBirth": "1999-12-15",
    },
    {
        "passengerId": "P-1008",
        "name": "Juan Sánchez López",
        "nationalId": "66554433H",
        "dateOfBirth": "1977-08-25",
    },
    {
        "passengerId": "P-1009",
        "name": "Lucía Martínez García",
        "nationalId": "77665544I",
        "dateOfBirth": "1990-02-10",
    },
    {
        "passengerId": "P-1010",
        "name": "Antonio García López",
        "nationalId": "88776655J",
        "dateOfBirth": "1980-06-05",
    },
    {
        "passengerId": "P-1011",
        "name": "Beatriz López Sánchez",
        "nationalId": "99887766K",
        "dateOfBirth": "1983-04-30",
    },
    {
        "passengerId": "P-1012",
        "name": "Carmen Martínez Rodríguez",
        "nationalId": "11001122L",
        "dateOfBirth": "1975-10-15",
    },
    {
        "passengerId": "P-1013",
        "name": "David Sánchez Martínez",
        "nationalId": "22110033M",
        "dateOfBirth": "1987-03-20",
    },
    {
        "passengerId": "P-1014",
        "name": "Elena García López",
        "nationalId": "33221100N",
        "dateOfBirth": "1978-07-25",
    },
    {
        "passengerId": "P-1015",
        "name": "Fernando López Martínez",
        "nationalId": "44332211O",
        "dateOfBirth": "1982-01-10",
    },
    {
        "passengerId": "P-1016",
        "name": "Gloria Martínez Sánchez",
        "nationalId": "55443322P",
        "dateOfBirth": "1984-09-05",
    },
    {
        "passengerId": "P-1017",
        "name": "Hugo Sánchez García",
        "nationalId": "66554433Q",
        "dateOfBirth": "1986-02-20",
    },
    {   
        "passengerId": "P-1018",
        "name": "Isabel García López",
        "nationalId": "77665544R",
        "dateOfBirth": "1976-12-15",
    },
    {
        "passengerId": "P-1019",
        "name": "Javier López Martínez",
        "nationalId": "88776655S",
        "dateOfBirth": "1981-08-25",
    },
    {
        "passengerId": "P-1020",
        "name": "Karla Martínez García",
        "nationalId": "99887766T",
        "dateOfBirth": "1989-02-10",
    }
]

def get_passenger_details(passenger_id):
    """Obtener detalles del pasajero por ID"""
    for passenger in passengers:
        if passenger["passengerId"] == passenger_id:
            return passenger
    return None

def calculate_age(date_of_birth, current_date=None):
    """Calcular la edad del pasajero a partir de su fecha de nacimiento"""
    if current_date is None:
        current_date = datetime.now()
    else:
        if isinstance(current_date, str):
            current_date = datetime.fromisoformat(current_date)
    
    birth_date = datetime.fromisoformat(date_of_birth)
    age = current_date.year - birth_date.year
    
    # Ajustar la edad si aún no ha pasado el cumpleaños de este año
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age

def get_arrived_passengers(current_time=None):
    """
    Obtener lista de pasajeros que han llegado al aeródromo
    
    Args:
        current_time (datetime, optional): Tiempo actual para comparar.
                                           Si es None, se usa el tiempo actual del sistema.
    
    Returns:
        list: Lista de pasajeros que han llegado con detalles adicionales
    """
    if current_time is None:
        current_time = datetime.now()
    elif isinstance(current_time, str):
        current_time = datetime.fromisoformat(current_time)
    
    arrived_passengers = []
    
    for flight in flights:
        arrival_time = datetime.fromisoformat(flight["arrivalTime"])
        
        # Si la hora de llegada ya pasó, los pasajeros han llegado
        if arrival_time <= current_time:
            # Obtener información del vuelo
            flight_info = {
                "flightId": flight["flightId"],
                "plateNumber": flight["plateNumber"],
                "origin": flight["origin"],
                "arrivalTime": flight["arrivalTime"]
            }
            
            # Agregar pasajeros que abordaron (excluir los cancelados)
            for passenger_id, status in flight["passengerIds"]:
                if status == 'Boarded':
                    passenger = get_passenger_details(passenger_id)
                    
                    if passenger:
                        # Calcular edad
                        age = calculate_age(passenger["dateOfBirth"], current_time)
                        
                        # Agregar detalles del pasajero
                        passenger_info = {
                            "passengerId": passenger["passengerId"],
                            "name": passenger["name"],
                            "nationalId": passenger["nationalId"],
                            "age": age,
                            "flight": flight_info
                        }
                        
                        arrived_passengers.append(passenger_info)
    
    return arrived_passengers

def display_arrived_passengers():
    """Mostrar la información de pasajeros que han llegado de manera formateada"""
    # Para propósitos de prueba, configuramos una fecha específica
    # En producción, se usaría datetime.now()
    test_current_time = "2025-03-02T13:00:00"  # Posterior a la llegada de ambos vuelos
    
    arrived_passengers = get_arrived_passengers(test_current_time)
    
    if not arrived_passengers:
        print("No hay pasajeros que hayan llegado al aeródromo hasta el momento.")
        return
    
    print("\n===================== PASAJEROS LLEGADOS AL AERÓDROMO =====================")
    print(f"Fecha de consulta: {datetime.fromisoformat(test_current_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print("=========================================================================")
    
    # Agrupar pasajeros por vuelo
    passengers_by_flight = {}
    for passenger in arrived_passengers:
        flight_id = passenger["flight"]["flightId"]
        if flight_id not in passengers_by_flight:
            passengers_by_flight[flight_id] = []
        passengers_by_flight[flight_id].append(passenger)
    
    # Mostrar pasajeros por vuelo
    for flight_id, flight_passengers in passengers_by_flight.items():
        flight_info = flight_passengers[0]["flight"]
        arrival_time = datetime.fromisoformat(flight_info["arrivalTime"])
        
        print(f"\nVUELO: {flight_id}")
        print(f"Origen: {flight_info['origin']}")
        print(f"Llegada: {arrival_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Aeronave: {flight_info['plateNumber']}")
        print("\nPasajeros:")
        print("-" * 80)
        print(f"{'ID':^10} | {'Nombre':^30} | {'DNI/Pasaporte':^15} | {'Edad':^5}")
        print("-" * 80)
        
        for passenger in flight_passengers:
            print(f"{passenger['passengerId']:^10} | {passenger['name']:<30} | {passenger['nationalId']:^15} | {passenger['age']:^5}")
    
    print("\n=========================================================================")
    print(f"Total de pasajeros llegados: {len(arrived_passengers)}")
    print("=========================================================================\n")

if __name__ == "__main__":
    display_arrived_passengers()
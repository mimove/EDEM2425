#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from initial_info import airplanes, flights


def get_airplane_details(plate_number):
    """Obtener detalles del avión por número de matrícula"""
    for airplane in airplanes:
        if airplane["plateNumber"] == plate_number:
            return airplane
    return None


def get_landed_flights(current_time=None):
    if current_time is None:
        current_time = datetime.now()
    landed_flights = []
    for flight in flights:
        arrival_time = datetime.fromisoformat(flight["arrivalTime"])
        if arrival_time < current_time:
            # Obtener información adicional del avión
            airplane = get_airplane_details(flight["plateNumber"])
            boarded_passengers = sum(1 for _, status in flight["passengerIds"] if status == 'Boarded')
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
    test_exact_timestamp = datetime.fromisoformat("2025-03-03T00:00:00")
    landed_flights = get_landed_flights(test_exact_timestamp)
    if not landed_flights:
        print("No hay vuelos aterrizados hasta el momento.")
        return
    print("\n===================== VUELOS ATERRIZADOS =====================")
    print(f"Fecha de consulta: {test_exact_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print("================================================================")

    for idx, flight in enumerate(landed_flights, 1):
        flight_id = flight["flightId"]
        arrival_time = datetime.fromisoformat(flight["arrivalTime"])
        print(f"\n{idx}. VUELO: {flight_id}")
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

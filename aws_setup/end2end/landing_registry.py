#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import uuid
from datetime import datetime, timedelta

# Directorio para almacenar los datos
DATA_DIR = "aerodrome_data"
FLIGHTS_FILE = os.path.join(DATA_DIR, "flights.json")
AIRPLANES_FILE = os.path.join(DATA_DIR, "airplanes.json")
LANDINGS_FILE = os.path.join(DATA_DIR, "landings.json")

# Datos de ejemplo para inicializar si no existen archivos
sample_airplanes = [
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

sample_flights = [
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

sample_landings = []  # Inicialmente vacío

def ensure_data_directory():
    """Asegurar que el directorio de datos existe"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_data(file_path, sample_data):
    """Cargar datos desde un archivo JSON o inicializar con datos de ejemplo"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error al leer el archivo {file_path}. Inicializando con datos de ejemplo.")
            return sample_data
    else:
        # Guardar datos de ejemplo en el archivo
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(sample_data, file, indent=4, ensure_ascii=False)
        return sample_data

def save_data(file_path, data):
    """Guardar datos en un archivo JSON"""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_aircraft_details(plate_number, airplanes):
    """Obtener detalles de una aeronave por su matrícula"""
    for airplane in airplanes:
        if airplane["plateNumber"] == plate_number:
            return airplane
    return None

def generate_flight_id():
    """Generar un ID único para un vuelo"""
    current_year = datetime.now().year
    return f"FL-{current_year}-{uuid.uuid4().hex[:6].upper()}"

def register_landing():
    """Registrar un aterrizaje en el aeródromo"""
    ensure_data_directory()
    airplanes = load_data(AIRPLANES_FILE, sample_airplanes)
    flights = load_data(FLIGHTS_FILE, sample_flights)
    landings = load_data(LANDINGS_FILE, sample_landings)
    
    print("\n" + "="*60)
    print("REGISTRO DE ATERRIZAJE EN EL AERÓDROMO")
    print("="*60)
    
    # Opción para seleccionar vuelo programado o no programado
    print("\n1. Registrar aterrizaje de vuelo programado")
    print("2. Registrar aterrizaje de vuelo no programado")
    option = input("\nSeleccione una opción: ")
    
    if option == "1":
        # Mostrar vuelos programados que aún no han aterrizado o no están registrados como aterrizados
        print("\nVuelos programados pendientes de registro de aterrizaje:")
        
        # Comprobar qué vuelos ya están registrados como aterrizados
        landed_flight_ids = {landing["flightId"] for landing in landings}
        
        pending_flights = []
        for idx, flight in enumerate(flights, 1):
            if flight["flightId"] not in landed_flight_ids:
                pending_flights.append(flight)
                arrival_time = datetime.fromisoformat(flight["arrivalTime"])
                print(f"{idx}. {flight['flightId']} - {flight['plateNumber']} - {flight['origin']} - Llegada programada: {arrival_time.strftime('%Y-%m-%d %H:%M')}")
        
        if not pending_flights:
            print("No hay vuelos programados pendientes de registro.")
            return
        
        selected_idx = input("\nSeleccione el número del vuelo a registrar (o 0 para cancelar): ")
        if not selected_idx.isdigit() or int(selected_idx) == 0:
            print("Operación cancelada.")
            return
        
        selected_idx = int(selected_idx)
        if selected_idx < 1 or selected_idx > len(pending_flights):
            print("Número inválido.")
            return
        
        selected_flight = pending_flights[selected_idx - 1]
        flight_id = selected_flight["flightId"]
        plate_number = selected_flight["plateNumber"]
        origin = selected_flight["origin"]
        scheduled_arrival = selected_flight["arrivalTime"]
        
    elif option == "2":
        # Registrar un vuelo no programado
        flight_id = generate_flight_id()
        
        # Solicitar matrícula del avión
        print("\nAeronaves registradas:")
        for idx, airplane in enumerate(airplanes, 1):
            print(f"{idx}. {airplane['plateNumber']} - {airplane['type']} - {airplane['ownerName']}")
        
        airplane_option = input("\nSeleccione el número de la aeronave (o 0 para ingresar una nueva): ")
        
        if airplane_option.isdigit() and int(airplane_option) > 0 and int(airplane_option) <= len(airplanes):
            selected_airplane = airplanes[int(airplane_option) - 1]
            plate_number = selected_airplane["plateNumber"]
        else:
            plate_number = input("Ingrese matrícula de la aeronave (EC-XXX): ").strip().upper()
            # Validar formato básico
            if not (plate_number.startswith("EC-") and len(plate_number) >= 5):
                print("Formato de matrícula inválido. Debe comenzar con 'EC-' seguido de al menos 3 caracteres.")
                return
        
        # Solicitar origen
        origin = input("Origen del vuelo: ").strip()
        if not origin:
            print("El origen es obligatorio.")
            return
        
        # Para vuelos no programados, no hay hora programada
        scheduled_arrival = None
    else:
        print("Opción inválida.")
        return
    
    # Solicitar información común para ambos tipos de vuelo
    # Hora real de aterrizaje
    print("\nHora de aterrizaje (dejar en blanco para usar la hora actual):")
    landing_date = input("Fecha (YYYY-MM-DD): ").strip()
    landing_time = input("Hora (HH:MM): ").strip()
    
    if landing_date and landing_time:
        try:
            actual_arrival = f"{landing_date}T{landing_time}:00"
            datetime.fromisoformat(actual_arrival)
        except ValueError:
            print("Formato de fecha u hora inválido. Usando la hora actual.")
            actual_arrival = datetime.now().isoformat()
    else:
        actual_arrival = datetime.now().isoformat()
    
    # Información adicional
    runway = input("Pista utilizada: ").strip() or "Principal"
    weather_conditions = input("Condiciones meteorológicas: ").strip() or "Despejado"
    
    try:
        passengers_count = int(input("Número de pasajeros: ").strip() or "0")
    except ValueError:
        print("Formato inválido para número de pasajeros. Usando 0 como valor predeterminado.")
        passengers_count = 0
    
    remarks = input("Observaciones: ").strip()
    
    # Crear registro de aterrizaje
    landing_record = {
        "landingId": f"LND-{uuid.uuid4().hex[:8].upper()}",
        "flightId": flight_id,
        "plateNumber": plate_number,
        "origin": origin,
        "scheduledArrival": scheduled_arrival,
        "actualArrival": actual_arrival,
        "runway": runway,
        "weatherConditions": weather_conditions,
        "passengersCount": passengers_count,
        "remarks": remarks,
        "registrationTimestamp": datetime.now().isoformat(),
        "registeredBy": "Jacinto"
    }
    
    # Si es un vuelo no programado, también creamos un registro de vuelo
    if option == "2":
        # Determinar hora de salida aproximada (2 horas después del aterrizaje por defecto)
        actual_arrival_dt = datetime.fromisoformat(actual_arrival)
        departure_time = (actual_arrival_dt + timedelta(hours=2)).isoformat()
        
        # Crear registro de vuelo
        new_flight = {
            "flightId": flight_id,
            "plateNumber": plate_number,
            "arrivalTime": actual_arrival,
            "departureTime": departure_time,
            "fuelConsumption": 0,  # Desconocido en este momento
            "occupiedSeats": passengers_count,
            "origin": origin,
            "destination": "Local",  # Por defecto
            "passengerIds": []  # Desconocidos en este momento
        }
        
        # Agregar a la lista de vuelos
        flights.append(new_flight)
        save_data(FLIGHTS_FILE, flights)
    
    # Agregar registro de aterrizaje
    landings.append(landing_record)
    save_data(LANDINGS_FILE, landings)
    
    print("\n" + "="*60)
    print(f"¡Aterrizaje del vuelo {flight_id} registrado exitosamente!")
    print(f"ID de registro: {landing_record['landingId']}")
    print("="*60 + "\n")

def search_landings():
    """Buscar y visualizar registros de aterrizajes"""
    ensure_data_directory()
    landings = load_data(LANDINGS_FILE, sample_landings)
    airplanes = load_data(AIRPLANES_FILE, sample_airplanes)
    
    if not landings:
        print("\nNo hay registros de aterrizajes en la base de datos.")
        return
    
    print("\n" + "="*60)
    print("BÚSQUEDA DE REGISTROS DE ATERRIZAJES")
    print("="*60)
    print("\n1. Ver todos los aterrizajes")
    print("2. Buscar por fecha")
    print("3. Buscar por matrícula de aeronave")
    print("4. Buscar por origen")
    
    option = input("\nSeleccione una opción: ")
    
    filtered_landings = []
    
    if option == "1":
        filtered_landings = landings
    elif option == "2":
        date_str = input("Ingrese fecha (YYYY-MM-DD): ").strip()
        try:
            search_date = datetime.fromisoformat(f"{date_str}T00:00:00")
            filtered_landings = [
                landing for landing in landings 
                if datetime.fromisoformat(landing["actualArrival"]).date() == search_date.date()
            ]
        except ValueError:
            print("Formato de fecha inválido.")
            return
    elif option == "3":
        plate_number = input("Ingrese matrícula de aeronave: ").strip().upper()
        filtered_landings = [landing for landing in landings if landing["plateNumber"] == plate_number]
    elif option == "4":
        origin = input("Ingrese origen: ").strip()
        filtered_landings = [landing for landing in landings if origin.lower() in landing["origin"].lower()]
    else:
        print("Opción inválida.")
        return
    
    if not filtered_landings:
        print("\nNo se encontraron registros que coincidan con los criterios de búsqueda.")
        return
    
    print("\n" + "="*100)
    print(f"RESULTADOS DE BÚSQUEDA: {len(filtered_landings)} registros encontrados")
    print("="*100)
    
    for landing in filtered_landings:
        actual_arrival = datetime.fromisoformat(landing["actualArrival"])
        aircraft = get_aircraft_details(landing["plateNumber"], airplanes)
        aircraft_type = aircraft["type"] if aircraft else "Desconocido"
        
        print(f"\nID Aterrizaje: {landing['landingId']}")
        print(f"Vuelo: {landing['flightId']}")
        print(f"Aeronave: {landing['plateNumber']} ({aircraft_type})")
        print(f"Origen: {landing['origin']}")
        print(f"Llegada: {actual_arrival.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if landing["scheduledArrival"]:
            scheduled_arrival = datetime.fromisoformat(landing["scheduledArrival"])
            delay = actual_arrival - scheduled_arrival
            delay_minutes = delay.total_seconds() / 60
            
            if delay_minutes > 15:
                print(f"Estado: Con retraso ({int(delay_minutes)} minutos)")
            elif delay_minutes < -15:
                print(f"Estado: Adelantado ({int(abs(delay_minutes))} minutos)")
            else:
                print("Estado: En hora")
        else:
            print("Estado: Vuelo no programado")
        
        print(f"Pista: {landing['runway']}")
        print(f"Condiciones: {landing['weatherConditions']}")
        print(f"Pasajeros: {landing['passengersCount']}")
        
        if landing["remarks"]:
            print(f"Observaciones: {landing['remarks']}")
        
        print(f"Registrado por: {landing['registeredBy']} el {datetime.fromisoformat(landing['registrationTimestamp']).strftime('%Y-%m-%d %H:%M')}")
        print("-"*100)
    
    print("\n" + "="*100)

def generate_report():
    """Generar un informe de aterrizajes por período"""
    ensure_data_directory()
    landings = load_data(LANDINGS_FILE, sample_landings)
    
    if not landings:
        print("\nNo hay registros de aterrizajes para generar un informe.")
        return
    
    print("\n" + "="*60)
    print("GENERACIÓN DE INFORME DE ATERRIZAJES")
    print("="*60)
    print("\n1. Informe diario")
    print("2. Informe semanal")
    print("3. Informe mensual")
    print("4. Informe personalizado")
    
    option = input("\nSeleccione una opción: ")
    
    today = datetime.now().date()
    
    if option == "1":
        # Informe diario (día actual)
        start_date = today
        end_date = today
        report_title = f"INFORME DIARIO DE ATERRIZAJES - {today.strftime('%d/%m/%Y')}"
    elif option == "2":
        # Informe semanal (últimos 7 días)
        start_date = today - timedelta(days=6)
        end_date = today
        report_title = f"INFORME SEMANAL DE ATERRIZAJES - {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}"
    elif option == "3":
        # Informe mensual (mes actual)
        start_date = today.replace(day=1)
        next_month = today.replace(day=28) + timedelta(days=4)
        end_date = next_month.replace(day=1) - timedelta(days=1)
        report_title = f"INFORME MENSUAL DE ATERRIZAJES - {start_date.strftime('%B %Y')}"
    elif option == "4":
        # Informe personalizado
        try:
            start_date_str = input("Fecha de inicio (YYYY-MM-DD): ").strip()
            start_date = datetime.fromisoformat(f"{start_date_str}T00:00:00").date()
            
            end_date_str = input("Fecha de fin (YYYY-MM-DD): ").strip()
            end_date = datetime.fromisoformat(f"{end_date_str}T23:59:59").date()
            
            if end_date < start_date:
                print("La fecha de fin debe ser posterior a la fecha de inicio.")
                return
            
            report_title = f"INFORME PERSONALIZADO DE ATERRIZAJES - {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}"
        except ValueError:
            print("Formato de fecha inválido.")
            return
    else:
        print("Opción inválida.")
        return
    
    # Filtrar aterrizajes por rango de fechas
    filtered_landings = []
    for landing in landings:
        landing_date = datetime.fromisoformat(landing["actualArrival"]).date()
        if start_date <= landing_date <= end_date:
            filtered_landings.append(landing)
    
    if not filtered_landings:
        print(f"\nNo hay registros de aterrizajes en el período seleccionado ({start_date} - {end_date}).")
        return
    
    # Ordenar por fecha
    filtered_landings.sort(key=lambda x: x["actualArrival"])
    
    # Agrupar por día
    landings_by_day = {}
    for landing in filtered_landings:
        landing_date = datetime.fromisoformat(landing["actualArrival"]).date()
        if landing_date not in landings_by_day:
            landings_by_day[landing_date] = []
        landings_by_day[landing_date].append(landing)
    
    # Estadísticas
    total_landings = len(filtered_landings)
    scheduled_landings = sum(1 for landing in filtered_landings if landing["scheduledArrival"])
    unscheduled_landings = total_landings - scheduled_landings
    
    delayed_landings = 0
    for landing in filtered_landings:
        if landing["scheduledArrival"]:
            actual = datetime.fromisoformat(landing["actualArrival"])
            scheduled = datetime.fromisoformat(landing["scheduledArrival"])
            if (actual - scheduled).total_seconds() > 900:  # 15 minutos
                delayed_landings += 1
    
    # Generar informe
    print("\n" + "="*100)
    print(report_title.center(100))
    print("="*100)
    
    for date in sorted(landings_by_day.keys()):
        day_landings = landings_by_day[date]
        print(f"\n{date.strftime('%A, %d de %B de %Y')}: {len(day_landings)} aterrizajes")
        print("-"*100)
        
        for landing in day_landings:
            arrival_time = datetime.fromisoformat(landing["actualArrival"]).strftime("%H:%M")
            print(f"{arrival_time} | Vuelo: {landing['flightId']} | Aeronave: {landing['plateNumber']} | Origen: {landing['origin']} | Pasajeros: {landing['passengersCount']}")
    
    print("\n" + "="*100)
    print("RESUMEN ESTADÍSTICO")
    print("="*100)
    print(f"Total de aterrizajes: {total_landings}")
    print(f"Aterrizajes programados: {scheduled_landings} ({scheduled_landings/total_landings*100:.1f}%)")
    print(f"Aterrizajes no programados: {unscheduled_landings} ({unscheduled_landings/total_landings*100:.1f}%)")
    
    if scheduled_landings > 0:
        print(f"Aterrizajes con retraso: {delayed_landings} ({delayed_landings/scheduled_landings*100:.1f}% de los programados)")
    
    # Promedio de pasajeros por aterrizaje
    total_passengers = sum(landing["passengersCount"] for landing in filtered_landings)
    avg_passengers = total_passengers / total_landings if total_landings > 0 else 0
    print(f"Promedio de pasajeros por vuelo: {avg_passengers:.1f}")
    
    print("\n" + "="*100)
    print(f"Informe generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*100)

def main_menu():
    """Mostrar menú principal"""
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE REGISTRO DE ATERRIZAJES")
        print("="*60)
        print("1. Registrar nuevo aterrizaje")
        print("2. Buscar registros de aterrizajes")
        print("3. Generar informe de aterrizajes")
        print("4. Salir")
        
        option = input("\nSeleccione una opción: ")
        
        if option == "1":
            register_landing()
        elif option == "2":
            search_landings()
        elif option == "3":
            generate_report()
        elif option == "4":
            print("\n¡Hasta pronto!")
            break
        else:
            print("\nOpción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main_menu()
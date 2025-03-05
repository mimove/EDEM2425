#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import uuid
from datetime import datetime, timedelta

# Directorio para almacenar los datos
DATA_DIR = "aerodrome_data"
PASSENGERS_FILE = os.path.join(DATA_DIR, "passengers.json")
FLIGHTS_FILE = os.path.join(DATA_DIR, "flights.json")
PASSENGER_LOGS_FILE = os.path.join(DATA_DIR, "passenger_logs.json")

# Datos de ejemplo para inicializar si no existen archivos
sample_passengers = [
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
    # Más pasajeros omitidos para mayor claridad
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

sample_passenger_logs = []  # Inicialmente vacío

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

def generate_passenger_id():
    """Generar un ID único para un pasajero"""
    return f"P-{uuid.uuid4().hex[:6].upper()}"

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

def validate_id_format(national_id):
    """Validar el formato básico del documento de identidad"""
    # Esto es una validación muy básica, puede adaptarse según los formatos específicos
    if len(national_id) < 3:
        return False, "El documento de identidad es demasiado corto."
    return True, ""

def validate_date_format(date_str):
    """Validar el formato de fecha (YYYY-MM-DD)"""
    try:
        datetime.fromisoformat(f"{date_str}T00:00:00")
        return True, ""
    except ValueError:
        return False, "Formato de fecha inválido. Use el formato YYYY-MM-DD."

def register_passenger_arrival_from_flight():
    """Registrar la llegada de pasajeros desde un vuelo programado"""
    ensure_data_directory()
    passengers = load_data(PASSENGERS_FILE, sample_passengers)
    flights = load_data(FLIGHTS_FILE, sample_flights)
    passenger_logs = load_data(PASSENGER_LOGS_FILE, sample_passenger_logs)
    
    print("\n" + "="*60)
    print("REGISTRO DE PASAJEROS DESDE VUELO PROGRAMADO")
    print("="*60)
    
    # Mostrar vuelos recientes que han aterrizado
    current_time = datetime.now()
    recent_flights = []
    
    print("\nVuelos recientes que han aterrizado:")
    for idx, flight in enumerate(flights, 1):
        arrival_time = datetime.fromisoformat(flight["arrivalTime"])
        
        # Considerar solo vuelos que han aterrizado en las últimas 24 horas
        if arrival_time <= current_time and (current_time - arrival_time).total_seconds() <= 86400:  # 24 horas en segundos
            recent_flights.append(flight)
            print(f"{idx}. {flight['flightId']} - Origen: {flight['origin']} - Llegada: {arrival_time.strftime('%Y-%m-%d %H:%M')}")
    
    if not recent_flights:
        print("No hay vuelos recientes que hayan aterrizado.")
        return
    
    selected_idx = input("\nSeleccione el número del vuelo (o 0 para cancelar): ")
    if not selected_idx.isdigit() or int(selected_idx) == 0:
        print("Operación cancelada.")
        return
    
    selected_idx = int(selected_idx)
    if selected_idx < 1 or selected_idx > len(recent_flights):
        print("Número inválido.")
        return
    
    selected_flight = recent_flights[selected_idx - 1]
    flight_id = selected_flight["flightId"]
    
    print(f"\nProcesando pasajeros del vuelo {flight_id}...")
    
    # Obtener listado de pasajeros del vuelo
    flight_passengers = []
    for passenger_id, status in selected_flight["passengerIds"]:
        if status == 'Boarded':  # Solo considerar los que abordaron
            passenger = next((p for p in passengers if p["passengerId"] == passenger_id), None)
            if passenger:
                flight_passengers.append(passenger)
    
    if not flight_passengers:
        print("No hay pasajeros registrados en este vuelo o todos han sido cancelados.")
        return
    
    print(f"\nPasajeros en el vuelo {flight_id}:")
    for idx, passenger in enumerate(flight_passengers, 1):
        age = calculate_age(passenger["dateOfBirth"])
        print(f"{idx}. {passenger['name']} - ID: {passenger['passengerId']} - DNI/Pasaporte: {passenger['nationalId']} - Edad: {age}")
    
    # Registrar llegada individual o masiva
    register_option = input("\n¿Desea registrar a todos los pasajeros (T) o individualmente (I)? ").strip().upper()
    
    if register_option == "T":
        # Registrar a todos los pasajeros
        for passenger in flight_passengers:
            # Verificar si ya está registrado
            already_registered = any(
                log["passengerId"] == passenger["passengerId"] and 
                log["flightId"] == flight_id and 
                log["type"] == "Arrival"
                for log in passenger_logs
            )
            
            if not already_registered:
                log_entry = {
                    "logId": f"LOG-{uuid.uuid4().hex[:8].upper()}",
                    "passengerId": passenger["passengerId"],
                    "name": passenger["name"],
                    "nationalId": passenger["nationalId"],
                    "flightId": flight_id,
                    "type": "Arrival",
                    "timestamp": datetime.now().isoformat(),
                    "notes": f"Llegada en vuelo {flight_id} desde {selected_flight['origin']}",
                    "registeredBy": "Jacinto"
                }
                
                passenger_logs.append(log_entry)
        
        save_data(PASSENGER_LOGS_FILE, passenger_logs)
        print(f"\nSe han registrado todos los pasajeros del vuelo {flight_id}.")
    
    elif register_option == "I":
        # Registrar pasajeros individualmente
        while True:
            passenger_idx = input("\nSeleccione el número del pasajero a registrar (o 0 para terminar): ")
            if not passenger_idx.isdigit() or int(passenger_idx) == 0:
                break
            
            passenger_idx = int(passenger_idx)
            if passenger_idx < 1 or passenger_idx > len(flight_passengers):
                print("Número inválido.")
                continue
            
            selected_passenger = flight_passengers[passenger_idx - 1]
            
            # Verificar si ya está registrado
            already_registered = any(
                log["passengerId"] == selected_passenger["passengerId"] and 
                log["flightId"] == flight_id and 
                log["type"] == "Arrival"
                for log in passenger_logs
            )
            
            if already_registered:
                print(f"El pasajero {selected_passenger['name']} ya ha sido registrado para este vuelo.")
                continue
            
            notes = input("Notas adicionales (opcional): ").strip()
            
            log_entry = {
                "logId": f"LOG-{uuid.uuid4().hex[:8].upper()}",
                "passengerId": selected_passenger["passengerId"],
                "name": selected_passenger["name"],
                "nationalId": selected_passenger["nationalId"],
                "flightId": flight_id,
                "type": "Arrival",
                "timestamp": datetime.now().isoformat(),
                "notes": notes or f"Llegada en vuelo {flight_id} desde {selected_flight['origin']}",
                "registeredBy": "Jacinto"
            }
            
            passenger_logs.append(log_entry)
            save_data(PASSENGER_LOGS_FILE, passenger_logs)
            
            print(f"Pasajero {selected_passenger['name']} registrado exitosamente.")
    
    else:
        print("Opción inválida.")

def register_individual_passenger():
    """Registrar un pasajero individual (puede ser nuevo o existente)"""
    ensure_data_directory()
    passengers = load_data(PASSENGERS_FILE, sample_passengers)
    passenger_logs = load_data(PASSENGER_LOGS_FILE, sample_passenger_logs)
    
    print("\n" + "="*60)
    print("REGISTRO INDIVIDUAL DE PASAJERO")
    print("="*60)
    
    # Preguntar si es un pasajero nuevo o existente
    is_new = input("\n¿Es un pasajero nuevo (N) o existente (E)? ").strip().upper()
    
    if is_new == "E":
        # Mostrar pasajeros existentes
        print("\nPasajeros registrados en el sistema:")
        for idx, passenger in enumerate(passengers, 1):
            print(f"{idx}. {passenger['name']} - ID: {passenger['passengerId']} - DNI/Pasaporte: {passenger['nationalId']}")
        
        selected_idx = input("\nSeleccione el número del pasajero (o 0 para cancelar): ")
        if not selected_idx.isdigit() or int(selected_idx) == 0:
            print("Operación cancelada.")
            return
        
        selected_idx = int(selected_idx)
        if selected_idx < 1 or selected_idx > len(passengers):
            print("Número inválido.")
            return
        
        selected_passenger = passengers[selected_idx - 1]
        passenger_id = selected_passenger["passengerId"]
        
    elif is_new == "N":
        # Registrar nuevo pasajero
        print("\nRegistro de nuevo pasajero:")
        name = input("Nombre completo: ").strip()
        if not name:
            print("El nombre es obligatorio.")
            return
        
        # Validar documento de identidad
        while True:
            national_id = input("DNI/Pasaporte: ").strip()
            is_valid, message = validate_id_format(national_id)
            if is_valid:
                # Verificar que no esté duplicado
                if any(p["nationalId"] == national_id for p in passengers):
                    print("Ya existe un pasajero con ese documento de identidad.")
                    retry = input("¿Desea intentar con otro documento (S/N)? ").strip().upper()
                    if retry != "S":
                        return
                else:
                    break
            else:
                print(f"Error: {message}")
                retry = input("¿Desea intentar de nuevo (S/N)? ").strip().upper()
                if retry != "S":
                    return
        
        # Validar fecha de nacimiento
        while True:
            date_of_birth = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
            is_valid, message = validate_date_format(date_of_birth)
            if is_valid:
                break
            print(f"Error: {message}")
            retry = input("¿Desea intentar de nuevo (S/N)? ").strip().upper()
            if retry != "S":
                return
        
        # Generar ID de pasajero
        passenger_id = generate_passenger_id()
        
        # Crear nuevo pasajero
        new_passenger = {
            "passengerId": passenger_id,
            "name": name,
            "nationalId": national_id,
            "dateOfBirth": date_of_birth
        }
        
        # Agregar a la lista de pasajeros
        passengers.append(new_passenger)
        save_data(PASSENGERS_FILE, passengers)
        
        selected_passenger = new_passenger
        print(f"\nNuevo pasajero registrado con ID: {passenger_id}")
    
    else:
        print("Opción inválida.")
        return
    
    # Registrar la llegada del pasajero
    print(f"\nRegistrando llegada de {selected_passenger['name']}:")
    
    # Información adicional
    flight_id = input("ID de vuelo (opcional): ").strip()
    origin = input("Origen (opcional): ").strip()
    notes = input("Notas adicionales (opcional): ").strip()
    
    arrival_info = {
        "logId": f"LOG-{uuid.uuid4().hex[:8].upper()}",
        "passengerId": passenger_id,
        "name": selected_passenger["name"],
        "nationalId": selected_passenger["nationalId"],
        "flightId": flight_id or "N/A",
        "origin": origin or "No especificado",
        "type": "Arrival",
        "timestamp": datetime.now().isoformat(),
        "notes": notes,
        "registeredBy": "Jacinto"
    }
    
    # Agregar al registro
    passenger_logs.append(arrival_info)
    save_data(PASSENGER_LOGS_FILE, passenger_logs)
    
    print("\n" + "="*60)
    print(f"¡Llegada del pasajero {selected_passenger['name']} registrada exitosamente!")
    print(f"ID de registro: {arrival_info['logId']}")
    print("="*60)

def search_passenger_logs():
    """Buscar y visualizar registros de pasajeros"""
    ensure_data_directory()
    passenger_logs = load_data(PASSENGER_LOGS_FILE, sample_passenger_logs)
    
    if not passenger_logs:
        print("\nNo hay registros de pasajeros en la base de datos.")
        return
    
    print("\n" + "="*60)
    print("BÚSQUEDA DE REGISTROS DE PASAJEROS")
    print("="*60)
    print("\n1. Ver todos los registros")
    print("2. Buscar por nombre")
    print("3. Buscar por documento de identidad")
    print("4. Buscar por fecha")
    print("5. Buscar por vuelo")
    
    option = input("\nSeleccione una opción: ")
    
    filtered_logs = []
    
    if option == "1":
        filtered_logs = passenger_logs
    elif option == "2":
        name = input("Ingrese nombre o parte del nombre: ").strip().lower()
        filtered_logs = [log for log in passenger_logs if name in log["name"].lower()]
    elif option == "3":
        national_id = input("Ingrese documento de identidad: ").strip()
        filtered_logs = [log for log in passenger_logs if log["nationalId"] == national_id]
    elif option == "4":
        date_str = input("Ingrese fecha (YYYY-MM-DD): ").strip()
        try:
            search_date = datetime.fromisoformat(f"{date_str}T00:00:00")
            filtered_logs = [
                log for log in passenger_logs 
                if datetime.fromisoformat(log["timestamp"]).date() == search_date.date()
            ]
        except ValueError:
            print("Formato de fecha inválido.")
            return
    elif option == "5":
        flight_id = input("Ingrese ID de vuelo: ").strip()
        filtered_logs = [log for log in passenger_logs if log["flightId"] == flight_id]
    else:
        print("Opción inválida.")
        return
    
    if not filtered_logs:
        print("\nNo se encontraron registros que coincidan con los criterios de búsqueda.")
        return
    
    print("\n" + "="*100)
    print(f"RESULTADOS DE BÚSQUEDA: {len(filtered_logs)} registros encontrados")
    print("="*100)
    
    # Ordenar por fecha/hora (más recientes primero)
    filtered_logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    for log in filtered_logs:
        timestamp = datetime.fromisoformat(log["timestamp"])
        
        print(f"\nID Registro: {log['logId']}")
        print(f"Pasajero: {log['name']} (ID: {log['passengerId']})")
        print(f"Documento: {log['nationalId']}")
        print(f"Tipo: {'Llegada' if log['type'] == 'Arrival' else 'Salida'}")
        print(f"Fecha/Hora: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if log["flightId"] != "N/A":
            print(f"Vuelo: {log['flightId']}")
        
        if "origin" in log and log["origin"] != "No especificado":
            print(f"Origen: {log['origin']}")
        
        if log["notes"]:
            print(f"Notas: {log['notes']}")
        
        print(f"Registrado por: {log['registeredBy']}")
        print("-"*100)

def generate_passenger_report():
    """Generar un informe de pasajeros por período"""
    ensure_data_directory()
    passenger_logs = load_data(PASSENGER_LOGS_FILE, sample_passenger_logs)
    
    if not passenger_logs:
        print("\nNo hay registros de pasajeros para generar un informe.")
        return
    
    print("\n" + "="*60)
    print("GENERACIÓN DE INFORME DE PASAJEROS")
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
        report_title = f"INFORME DIARIO DE PASAJEROS - {today.strftime('%d/%m/%Y')}"
    elif option == "2":
        # Informe semanal (últimos 7 días)
        start_date = today - timedelta(days=6)
        end_date = today
        report_title = f"INFORME SEMANAL DE PASAJEROS - {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}"
    elif option == "3":
        # Informe mensual (mes actual)
        start_date = today.replace(day=1)
        next_month = today.replace(day=28) + timedelta(days=4)
        end_date = next_month.replace(day=1) - timedelta(days=1)
        report_title = f"INFORME MENSUAL DE PASAJEROS - {start_date.strftime('%B %Y')}"
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
            
            report_title = f"INFORME PERSONALIZADO DE PASAJEROS - {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}"
        except ValueError:
            print("Formato de fecha inválido.")
            return
    else:
        print("Opción inválida.")
        return
    
    # Filtrar registros por rango de fechas
    filtered_logs = []
    for log in passenger_logs:
        log_date = datetime.fromisoformat(log["timestamp"]).date()
        if start_date <= log_date <= end_date:
            filtered_logs.append(log)
    
    if not filtered_logs:
        print(f"\nNo hay registros de pasajeros en el período seleccionado ({start_date} - {end_date}).")
        return
    
    # Ordenar por fecha
    filtered_logs.sort(key=lambda x: x["timestamp"])
    
    # Agrupar por día
    logs_by_day = {}
    for log in filtered_logs:
        log_date = datetime.fromisoformat(log["timestamp"]).date()
        if log_date not in logs_by_day:
            logs_by_day[log_date] = []
        logs_by_day[log_date].append(log)
    
    # Generar informe
    print("\n" + "="*100)
    print(report_title.center(100))
    print("="*100)
    
    total_arrivals = 0
    
    for date in sorted(logs_by_day.keys()):
        day_logs = logs_by_day[date]
        day_arrivals = sum(1 for log in day_logs if log["type"] == "Arrival")
        total_arrivals += day_arrivals
        
        print(f"\n{date.strftime('%A, %d de %B de %Y')}: {day_arrivals} llegadas")
        print("-"*100)
        
        if day_arrivals > 0:
            print(f"{'Hora':^10} | {'Nombre':^30} | {'Documento':^15} | {'Vuelo':^12}")
            print("-"*100)
            
            for log in day_logs:
                if log["type"] == "Arrival":
                    arrival_time = datetime.fromisoformat(log["timestamp"]).strftime("%H:%M")
                    flight_id = log["flightId"] if log["flightId"] != "N/A" else "-"
                    print(f"{arrival_time:^10} | {log['name']:<30} | {log['nationalId']:^15} | {flight_id:^12}")
    
    print("\n" + "="*100)
    print("RESUMEN ESTADÍSTICO")
    print("="*100)
    print(f"Total de llegadas de pasajeros: {total_arrivals}")
    
    # Calcular promedio diario
    days_in_period = (end_date - start_date).days + 1
    avg_daily_arrivals = total_arrivals / days_in_period
    print(f"Promedio diario de llegadas: {avg_daily_arrivals:.1f}")
    
    print("\n" + "="*100)
    print(f"Informe generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*100)

def main_menu():
    """Mostrar menú principal"""
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE REGISTRO DE PASAJEROS")
        print("="*60)
        print("1. Registrar pasajeros desde vuelo")
        print("2. Registrar pasajero individual")
        print("3. Buscar registros de pasajeros")
        print("4. Generar informe de pasajeros")
        print("5. Salir")
        
        option = input("\nSeleccione una opción: ")
        
        if option == "1":
            register_passenger_arrival_from_flight()
        elif option == "2":
            register_individual_passenger()
        elif option == "3":
            search_passenger_logs()
        elif option == "4":
            generate_passenger_report()
        elif option == "5":
            print("\n¡Hasta pronto!")
            break
        else:
            print("\nOpción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main_menu()
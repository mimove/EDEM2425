#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
import os
import uuid

# Directorio para almacenar los datos
DATA_DIR = "aerodrome_data"
AIRPLANES_FILE = os.path.join(DATA_DIR, "airplanes.json")
HANGARS_FILE = os.path.join(DATA_DIR, "hangars.json")

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
        "fuel_capacity": 700,
        "registrationDate": "2024-12-15T10:30:00",
        "status": "Active"
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
        "fuel_capacity": 1000,
        "registrationDate": "2024-12-20T14:45:00",
        "status": "Active"
    }
]

sample_hangars = [
    {
        "hangarId": "H-01",
        "name": "Hangar Principal",
        "capacity": 5,
        "location": "Zona Norte",
        "supervisor": "Miguel Sánchez"
    },
    {
        "hangarId": "H-02",
        "name": "Hangar Secundario",
        "capacity": 3,
        "location": "Zona Sur",
        "supervisor": "Laura Gómez"
    },
    {
        "hangarId": "H-03",
        "name": "Hangar de Mantenimiento",
        "capacity": 2,
        "location": "Zona Técnica",
        "supervisor": "Carlos Ruiz"
    }
]

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

def validate_plate_number(plate_number, airplanes):
    """Validar que el número de matrícula sea único y tenga el formato correcto"""
    # Verificar formato (ejemplo: EC-XXX donde X puede ser letra o número)
    if not (plate_number.startswith("EC-") and len(plate_number) >= 5):
        return False, "El número de matrícula debe comenzar con 'EC-' seguido de al menos 3 caracteres."
    
    # Verificar que no exista ya
    if any(airplane["plateNumber"] == plate_number for airplane in airplanes):
        return False, f"Ya existe un avión con la matrícula {plate_number}."
    
    return True, ""

def validate_hangar(hangar_id, hangars, airplanes):
    """Validar que el hangar exista y tenga espacio disponible"""
    # Verificar que el hangar exista
    hangar = next((h for h in hangars if h["hangarId"] == hangar_id), None)
    if not hangar:
        return False, f"El hangar con ID {hangar_id} no existe."
    
    # Contar aviones actualmente en el hangar
    airplanes_in_hangar = sum(1 for a in airplanes if a["hangarId"] == hangar_id and a["status"] == "Active")
    
    # Verificar capacidad
    if airplanes_in_hangar >= hangar["capacity"]:
        return False, f"El hangar {hangar_id} está lleno (capacidad: {hangar['capacity']})."
    
    return True, ""

def register_airplane(is_new=True):
    """Registrar un avión nuevo o actualizar uno existente en un hangar"""
    # Cargar datos existentes
    ensure_data_directory()
    airplanes = load_data(AIRPLANES_FILE, sample_airplanes)
    hangars = load_data(HANGARS_FILE, sample_hangars)
    
    print("\n" + "="*50)
    if is_new:
        print("REGISTRO DE NUEVO AVIÓN EN HANGAR")
    else:
        print("ACTUALIZACIÓN DE REGISTRO DE AVIÓN EN HANGAR")
    print("="*50)
    
    if not is_new:
        # Mostrar aviones existentes
        print("\nAviones registrados:")
        for idx, airplane in enumerate(airplanes, 1):
            status_text = "Activo" if airplane["status"] == "Active" else "Inactivo"
            print(f"{idx}. {airplane['plateNumber']} - {airplane['type']} ({status_text}) - Hangar: {airplane['hangarId']}")
        
        selected_idx = input("\nSeleccione el número del avión a actualizar (o 0 para cancelar): ")
        if not selected_idx.isdigit() or int(selected_idx) == 0:
            print("Operación cancelada.")
            return
        
        selected_idx = int(selected_idx)
        if selected_idx < 1 or selected_idx > len(airplanes):
            print("Número inválido.")
            return
        
        # Obtener el avión seleccionado
        airplane = airplanes[selected_idx - 1]
        plate_number = airplane["plateNumber"]
        
        print(f"\nActualizando información para el avión {plate_number}")
    else:
        # Solicitar datos para el nuevo avión
        while True:
            plate_number = input("\nNúmero de matrícula (EC-XXX): ").strip().upper()
            is_valid, message = validate_plate_number(plate_number, airplanes)
            if is_valid:
                break
            print(f"Error: {message}")
    
    # Mostrar hangares disponibles
    print("\nHangares disponibles:")
    for hangar in hangars:
        airplanes_in_hangar = sum(1 for a in airplanes if a["hangarId"] == hangar["hangarId"] and a["status"] == "Active")
        available_space = hangar["capacity"] - airplanes_in_hangar
        print(f"{hangar['hangarId']} - {hangar['name']} ({available_space} espacios disponibles de {hangar['capacity']})")
    
    # Solicitar el ID del hangar
    while True:
        hangar_id = input("\nID del hangar para asignar el avión: ").strip().upper()
        is_valid, message = validate_hangar(hangar_id, hangars, airplanes)
        if is_valid:
            break
        print(f"Error: {message}")
    
    if is_new:
        # Solicitar datos adicionales para un nuevo avión
        airplane_type = input("Tipo de avión: ").strip()
        capacity = input("Capacidad de pasajeros: ")
        
        try:
            capacity = int(capacity)
        except ValueError:
            print("La capacidad debe ser un número entero. Usando valor predeterminado de 1.")
            capacity = 1
        
        fuel_capacity = input("Capacidad de combustible: ")
        
        try:
            fuel_capacity = int(fuel_capacity)
        except ValueError:
            print("La capacidad de combustible debe ser un número entero. Usando valor predeterminado de 100.")
            fuel_capacity = 100
        
        owner_name = input("Nombre del propietario: ").strip()
        
        # Generar un nuevo ID de propietario si no existe
        owner_id = f"O-{uuid.uuid4().hex[:5].upper()}"
        
        # Fechas de mantenimiento
        last_maintenance = input("Última fecha de mantenimiento (YYYY-MM-DD): ").strip()
        try:
            datetime.fromisoformat(last_maintenance)
        except ValueError:
            today = datetime.now().strftime("%Y-%m-%d")
            print(f"Formato de fecha incorrecto. Usando la fecha actual: {today}")
            last_maintenance = today
        
        next_maintenance = input("Próxima fecha de mantenimiento (YYYY-MM-DD): ").strip()
        try:
            datetime.fromisoformat(next_maintenance)
        except ValueError:
            next_year = datetime.now().replace(year=datetime.now().year + 1).strftime("%Y-%m-%d")
            print(f"Formato de fecha incorrecto. Usando un año a partir de hoy: {next_year}")
            next_maintenance = next_year
        
        # Crear nuevo registro de avión
        new_airplane = {
            "plateNumber": plate_number,
            "type": airplane_type,
            "lastMaintenanceDate": last_maintenance,
            "nextMaintenanceDate": next_maintenance,
            "capacity": capacity,
            "ownerId": owner_id,
            "ownerName": owner_name,
            "hangarId": hangar_id,
            "fuel_capacity": fuel_capacity,
            "registrationDate": datetime.now().isoformat(),
            "status": "Active"
        }
        
        # Agregar nuevo avión a la lista
        airplanes.append(new_airplane)
    else:
        # Actualizar información del avión existente
        new_hangar_id = hangar_id  # Nuevo hangar asignado
        status = input("Estado del avión (Active/Inactive): ").strip().capitalize()
        if status not in ["Active", "Inactive"]:
            print("Estado inválido. Usando 'Active' como predeterminado.")
            status = "Active"
        
        # Actualizar información
        airplane["hangarId"] = new_hangar_id
        airplane["status"] = status
        airplane["lastUpdateDate"] = datetime.now().isoformat()
    
    # Guardar datos actualizados
    save_data(AIRPLANES_FILE, airplanes)
    
    print("\n" + "="*50)
    if is_new:
        print(f"¡Avión {plate_number} registrado exitosamente en el hangar {hangar_id}!")
    else:
        print(f"¡Información del avión {plate_number} actualizada exitosamente!")
    print("="*50 + "\n")

def list_airplanes_in_hangars():
    """Listar todos los aviones en los hangares"""
    # Cargar datos existentes
    ensure_data_directory()
    airplanes = load_data(AIRPLANES_FILE, sample_airplanes)
    hangars = load_data(HANGARS_FILE, sample_hangars)
    
    print("\n" + "="*50)
    print("LISTADO DE AVIONES EN HANGARES")
    print("="*50)
    
    # Agrupar aviones por hangar
    airplanes_by_hangar = {}
    for airplane in airplanes:
        if airplane["status"] == "Active":  # Solo mostrar aviones activos
            hangar_id = airplane["hangarId"]
            if hangar_id not in airplanes_by_hangar:
                airplanes_by_hangar[hangar_id] = []
            airplanes_by_hangar[hangar_id].append(airplane)
    
    # Mostrar aviones por hangar
    for hangar in hangars:
        hangar_id = hangar["hangarId"]
        hangar_name = hangar["name"]
        print(f"\nHangar: {hangar_id} - {hangar_name}")
        print("-" * 80)
        
        if hangar_id in airplanes_by_hangar and airplanes_by_hangar[hangar_id]:
            print(f"{'Matrícula':<10} | {'Tipo':<25} | {'Propietario':<25} | {'Último Mant.':<12} | {'Próximo Mant.':<12}")
            print("-" * 80)
            
            for airplane in airplanes_by_hangar[hangar_id]:
                print(f"{airplane['plateNumber']:<10} | {airplane['type']:<25} | {airplane['ownerName']:<25} | {airplane['lastMaintenanceDate']:<12} | {airplane['nextMaintenanceDate']:<12}")
        else:
            print("No hay aviones registrados en este hangar.")
    
    print("\n" + "="*50)
    total_airplanes = sum(len(airplanes) for airplanes in airplanes_by_hangar.values())
    print(f"Total de aviones registrados en hangares: {total_airplanes}")
    print("="*50 + "\n")

def main_menu():
    """Mostrar menú principal"""
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE REGISTRO DE AVIONES EN HANGARES")
        print("="*50)
        print("1. Registrar nuevo avión")
        print("2. Actualizar registro de avión existente")
        print("3. Listar aviones en hangares")
        print("4. Salir")
        
        option = input("\nSeleccione una opción: ")
        
        if option == "1":
            register_airplane(is_new=True)
        elif option == "2":
            register_airplane(is_new=False)
        elif option == "3":
            list_airplanes_in_hangars()
        elif option == "4":
            print("\n¡Hasta pronto!")
            break
        else:
            print("\nOpción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main_menu()
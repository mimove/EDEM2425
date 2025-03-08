from initial_info import airplanes, passengers, flights 
import logging
import os

import psycopg2
from dotenv import load_dotenv # Importa las variables del archivo .env lo que se escribe como dotenv

logging.basicConfig(level=logging.INFO) # Ajustes predeterminados para el logging

load_dotenv() # Carga las variables de entorno desde el archivo.env

RDS_HOST = os.environ['RDS_HOST']
RDS_PORT = os.environ['RDS_PORT']
RDS_USER = os.environ['RDS_USER']
RDS_PASSWORD = os.environ['RDS_PASSWORD']
RDS_DB = os.environ['RDS_DB']

def connect_to_postgres_rds() -> psycopg2.connect:
    conn= psycopg2.connect(
        host= RDS_HOST,
        port= RDS_PORT, 
        user= RDS_USER,
        password= RDS_PASSWORD,
        database=RDS_DB
    )
    return conn

def create_tables(conn):
    """
    Se crean las tablas necesarias para la gestión de:
      - aviones
      - pasajeros
      - vuelos
      - relación entre pasajeros y vuelos
      
    Se configura ON DELETE CASCADE en las claves foráneas para que,
    al eliminar un registro padre, se eliminen automáticamente los registros hijos.
    """
    with conn.cursor() as cur:
        # Crear la tabla de aviones
        cur.execute('''
            CREATE TABLE IF NOT EXISTS airplanes (
                plateNumber VARCHAR PRIMARY KEY, 
                type VARCHAR NOT NULL, 
                lastMaintenanceDate DATE,
                nextMaintenanceDate DATE,
                capacity INT,
                ownerId VARCHAR,
                ownerName VARCHAR,
                hangarId VARCHAR,
                fuel_capacity FLOAT
            );
        ''')

        # Crear la tabla de pasajeros
        cur.execute('''
            CREATE TABLE IF NOT EXISTS passengers (
                passengerId VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                nationalId VARCHAR NOT NULL,
                dateOfBirth DATE
            );
        ''')

        # Crear la tabla de vuelos referenciando aviones con borrado en cascada
        cur.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                flightId VARCHAR PRIMARY KEY,
                plateNumber VARCHAR,
                departureTime DATE,
                arrivalTime DATE,
                fuelConsumption FLOAT,
                occupiedSeats INT,
                origin VARCHAR,
                destination VARCHAR,
                CONSTRAINT fk_airplanes FOREIGN KEY (plateNumber)
                    REFERENCES airplanes (plateNumber)
                    ON DELETE CASCADE
            );
        ''')

        # Crear la tabla de relación flight_passengers con claves foráneas y borrado en cascada.
        # Así, si se elimina un vuelo o un pasajero, se eliminan las relaciones correspondientes.
        cur.execute('''
            CREATE TABLE IF NOT EXISTS flight_passengers (
                flightId VARCHAR,
                passengerId VARCHAR,
                status VARCHAR,
                PRIMARY KEY (flightId, passengerId),
                CONSTRAINT fk_flights FOREIGN KEY (flightId)
                    REFERENCES flights (flightId)
                    ON DELETE CASCADE,
                CONSTRAINT fk_passengers FOREIGN KEY (passengerId)
                    REFERENCES passengers (passengerId)
                    ON DELETE CASCADE
            );
        ''')

    conn.commit()


def insert_airplanes(conn, airplane_list):
    with conn.cursor() as cur: 
        for airplane in airplane_list:
            cur.execute('''
                INSERT INTO airplanes 
                    (plateNumber, type, lastMaintenanceDate nextMaintenanceDate, capacity, ownerId, ownerName, hangarId, fuel_capacity)

                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON CONFLICT (plateNumber) DO NOTHING
                ''',
                (
                    airplane["plateNumber"],
                    airplane["type"],
                    airplane["lastMaintenanceDate"],
                    airplane["nextMaintenanceDate"],
                    airplane["capacity"],
                    airplane["ownerId"],
                    airplane["ownerName"],
                    airplane["hangarId"],
                    airplane["fuel_capacity"]))
        conn.commit()

def insert_passengers(conn, passengers_list):
    with conn.cursor() as cur:
            for p in passengers_list:
                cur.execute('''
                    Insert into passengers
                            (passengerId,
                            name,
                            nationalId,
                            dateOfBirth)
                            Values (%s, %s,%s,%s )
                            ON CONFLICT (passengerId) DO NOTHING
                            ''', (
                                p["passengerId"],
                                p["name"],
                                p["nationalId"],
                                p["dateOfBirth"]
                            ))
                conn.commit()

def insert_flights(conn, flight_list):
    with conn.cursor() as cur:
        for f in flight_list:
            cur.execute("""
                INSERT INTO flights (
                    flightId,
                    plateNumber,
                    arrivalTime,
                    departureTime,
                    fuelConsumption,
                    occupiedSeats,
                    origin,
                    destination
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (flightId) DO NOTHING
            """, (
                f["flightId"],
                f["plateNumber"],
                f["arrivalTime"],
                f["departureTime"],
                f["fuelConsumption"],
                f["occupiedSeats"],
                f["origin"],
                f["destination"]
            ))
        conn.commit()


def insert_flight_passengers(conn, flight_list):
    """
    Inserta la relación de pasajeros por vuelo.
    flight['passengerIds'] es una lista de tuplas: [(passengerId, status), ...]
    """
    with conn.cursor() as cur:
        for f in flight_list:
            flight_id = f["flightId"]
            for (passenger_id, status) in f["passengerIds"]:
                cur.execute("""
                    INSERT INTO flight_passengers (
                        flightId,
                        passengerId,
                        status
                    )
                    VALUES (%s, %s, %s)
                    ON CONFLICT (flightId, passengerId) DO NOTHING
                """, (flight_id, passenger_id, status))
        conn.commit()


if __name__ == "__main__":
    logging.info("Conectando a la base de datos RDS...")
    conn = connect_to_postgres_rds()
    logging.info("Conexión establecida.")

    logging.info("Creando tablas si no existen...")
    create_tables(conn)
    logging.info("Tablas creadas.")

    logging.info("Insertando datos de aviones...")
    insert_airplanes(conn, airplanes)
    logging.info("Datos de aviones insertados.")

    logging.info("Insertando datos de pasajeros...")
    insert_passengers(conn, passengers)
    logging.info("Datos de pasajeros insertados.")

    logging.info("Insertando datos de vuelos...")
    insert_flights(conn, flights)
    logging.info("Datos de vuelos insertados.")

    logging.info("Insertando relaciones vuelo-pasajeros...")
    insert_flight_passengers(conn, flights)
    logging.info("Relaciones insertadas.")

    conn.close()
    logging.info("Conexión cerrada.")
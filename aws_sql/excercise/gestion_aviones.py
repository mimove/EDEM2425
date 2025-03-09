import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
from datetime import date
import pandas as pd

# Cargar variables de entorno
load_dotenv()

RDS_HOST = os.environ.get('RDS_HOST')
RDS_PORT = os.environ.get('RDS_PORT')
RDS_USER = os.environ.get('RDS_USER')
RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
RDS_DB = os.environ.get('RDS_DB')

def connect_to_postgres_rds():
    """
    Conecta a la base de datos PostgreSQL usando las variables de entorno.
    """
    conn = psycopg2.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB
    )
    return conn

def get_landed_airplanes(conn):
    """
    Devuelve los aviones que han aterrizado (arrivalTime <= NOW()).
    """
    query = """
        SELECT DISTINCT a.*
        FROM airplanes a
        JOIN flights f ON a.plateNumber = f.plateNumber
        WHERE f.arrivalTime <= NOW();
    """
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=columns)

def get_in_flight_airplanes(conn):
    """
    Devuelve los aviones en vuelo (departureTime <= NOW() < arrivalTime).
    """
    query = """
        SELECT DISTINCT a.*
        FROM airplanes a
        JOIN flights f ON a.plateNumber = f.plateNumber
        WHERE f.departureTime <= NOW()
          AND f.arrivalTime > NOW();
    """
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=columns)

def get_upcoming_airplanes(conn):
    """
    Devuelve los aviones que van a salir (departureTime > NOW()).
    """
    query = """
        SELECT DISTINCT a.*
        FROM airplanes a
        JOIN flights f ON a.plateNumber = f.plateNumber
        WHERE f.departureTime > NOW();
    """
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=columns)



def insert_airplane(conn, airplane):
    """
    Inserta un nuevo avión en la tabla airplanes.
    Evita duplicados con ON CONFLICT (plateNumber).
    """
    query = """
        INSERT INTO airplanes (
            plateNumber, type, lastMaintenanceDate, nextMaintenanceDate, capacity, 
            ownerId, ownerName, hangarId, fuel_capacity
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (plateNumber) DO NOTHING;
    """
    with conn.cursor() as cur:
        cur.execute(query, (
            airplane["plateNumber"],
            airplane["type"],
            airplane["lastMaintenanceDate"],
            airplane["nextMaintenanceDate"],
            airplane["capacity"],
            airplane["ownerId"],
            airplane["ownerName"],
            airplane["hangarId"],
            airplane["fuel_capacity"],
        ))
    conn.commit()

def insert_passenger(conn, passenger):
    """
    Inserta un nuevo pasajero en la tabla passengers.
    Evita duplicados con ON CONFLICT (passengerId).
    """
    query = """
        INSERT INTO passengers (
            passengerId, name, nationalId, dateOfBirth
        ) VALUES (%s, %s, %s, %s)
        ON CONFLICT (passengerId) DO NOTHING;
    """
    with conn.cursor() as cur:
        cur.execute(query, (
            passenger["passengerId"],
            passenger["name"],
            passenger["nationalId"],
            passenger["dateOfBirth"],
        ))
    conn.commit()

def insert_flight(conn, flight):
    """
    Inserta un nuevo vuelo en la tabla flights.
    Evita duplicados con ON CONFLICT (flightId).
    Se asume que departureTime y arrivalTime son TIMESTAMP en la BD,
    y que flight['departureTime'] / flight['arrivalTime'] son cadenas '2025-03-01T09:30:00'.
    """
    query = """
        INSERT INTO flights (
            flightId, plateNumber, departureTime, arrivalTime,
            fuelConsumption, occupiedSeats, origin, destination
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (flightId) DO NOTHING;
    """
    with conn.cursor() as cur:
        cur.execute(query, (
            flight["flightId"],
            flight["plateNumber"],
            flight["departureTime"],
            flight["arrivalTime"],
            flight["fuelConsumption"],
            flight["occupiedSeats"],
            flight["origin"],
            flight["destination"]
        ))
    conn.commit()

def register_passenger_in_flight(conn, flight_id, passenger_id, status):
    """
    Registra o actualiza el estado de un pasajero en un vuelo.
    El estado (status) puede ser 'Boarded', 'Cancelled', 'Checked-in', 'No-show', etc.
    """
    query = """
        INSERT INTO flight_passengers (flightId, passengerId, status)
        VALUES (%s, %s, %s)
        ON CONFLICT (flightId, passengerId)
        DO UPDATE SET status = EXCLUDED.status;
    """
    with conn.cursor() as cur:
        cur.execute(query, (flight_id, passenger_id, status))
    conn.commit()

def page_ver_aviones(conn):
    st.subheader("Ver aviones según estado")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Aviones aterrizados (arrivalTime <= NOW)"):
            try:
                df_landed = get_landed_airplanes(conn)
                if not df_landed.empty:
                    st.dataframe(df_landed)
                else:
                    st.info("No se encontraron aviones aterrizados.")
            except Exception as e:
                st.error(f"Error al obtener los datos: {e}")

    with col2:
        if st.button("Aviones en vuelo (departure <= NOW < arrival)"):
            try:
                df_in_flight = get_in_flight_airplanes(conn)
                if not df_in_flight.empty:
                    st.dataframe(df_in_flight)
                else:
                    st.info("No se encontraron aviones en vuelo.")
            except Exception as e:
                st.error(f"Error al obtener los datos: {e}")

    with col3:
        if st.button("Aviones por salir (departure > NOW)"):
            try:
                df_upcoming = get_upcoming_airplanes(conn)
                if not df_upcoming.empty:
                    st.dataframe(df_upcoming)
                else:
                    st.info("No se encontraron aviones próximos a salir.")
            except Exception as e:
                st.error(f"Error al obtener los datos: {e}")

def page_add_airplane(conn):    
    st.subheader("Añadir un nuevo avión")
    with st.form("form_add_airplane"):
        plate_number = st.text_input("Número de matrícula")
        airplane_type = st.text_input("Tipo de avión")
        last_maintenance_date = st.date_input("Fecha de última mantención", date.today())
        next_maintenance_date = st.date_input("Fecha de próxima mantención", date.today())
        capacity = st.number_input("Capacidad", min_value=1, step=1)
        owner_id = st.text_input("ID del propietario")
        owner_name = st.text_input("Nombre del propietario")
        hangar_id = st.text_input("ID del hangar")
        fuel_capacity = st.number_input("Capacidad de combustible", min_value=0.0, step=1.0)
        
        submitted_plane = st.form_submit_button("Añadir avión")
        if submitted_plane:
            if not plate_number or not airplane_type:
                st.error("Por favor, complete al menos el número de matrícula y el tipo de avión.")
            else:
                new_airplane = {
                    "plateNumber": plate_number,
                    "type": airplane_type,
                    "lastMaintenanceDate": last_maintenance_date,
                    "nextMaintenanceDate": next_maintenance_date,
                    "capacity": capacity,
                    "ownerId": owner_id,
                    "ownerName": owner_name,
                    "hangarId": hangar_id,
                    "fuel_capacity": fuel_capacity
                }
                try:
                    insert_airplane(conn, new_airplane)
                    st.success("Avión añadido correctamente.")
                except Exception as e:
                    st.error(f"Error al añadir el avión: {e}")

def page_add_passenger(conn):
    st.subheader("Añadir un nuevo pasajero")
    with st.form("form_add_passenger"):
        new_passenger_id = st.text_input("Passenger ID (p. ej.: P-1015)")
        new_passenger_name = st.text_input("Nombre del pasajero")
        new_passenger_nationalid = st.text_input("Documento de identidad")
        new_passenger_dob = st.date_input("Fecha de nacimiento", date.today())

        submitted_passenger_data = st.form_submit_button("Añadir pasajero")
        if submitted_passenger_data:
            if not new_passenger_id or not new_passenger_name or not new_passenger_nationalid:
                st.error("Por favor, complete todos los campos obligatorios.")
            else:
                passenger_data = {
                    "passengerId": new_passenger_id,
                    "name": new_passenger_name,
                    "nationalId": new_passenger_nationalid,
                    "dateOfBirth": new_passenger_dob
                }
                try:
                    insert_passenger(conn, passenger_data)
                    st.success(f"Pasajero {new_passenger_id} añadido correctamente.")
                except Exception as e:
                    st.error(f"Error al añadir pasajero: {e}")

def page_add_flight(conn):
    st.subheader("Añadir un nuevo vuelo")
    with st.form("form_add_flight"):
        new_flight_id = st.text_input("Flight ID (p. ej.: FL-2025-001)")
        flight_plate = st.text_input("Matrícula del avión (plateNumber)")
        departure_str = st.text_input("Fecha/Hora de salida (YYYY-MM-DDTHH:MM:SS)", "2025-03-01T09:30:00")
        arrival_str = st.text_input("Fecha/Hora de llegada (YYYY-MM-DDTHH:MM:SS)", "2025-03-01T14:45:00")
        fuel_consumption = st.number_input("Consumo de combustible", min_value=0.0, step=1.0)
        occupied_seats = st.number_input("Asientos ocupados", min_value=0, step=1)
        origin = st.text_input("Origen")
        destination = st.text_input("Destino")

        submitted_flight = st.form_submit_button("Añadir vuelo")
        if submitted_flight:
            if not new_flight_id or not flight_plate or not departure_str or not arrival_str:
                st.error("Por favor, complete los campos obligatorios.")
            else:
                new_flight = {
                    "flightId": new_flight_id,
                    "plateNumber": flight_plate,
                    "departureTime": departure_str,
                    "arrivalTime": arrival_str,
                    "fuelConsumption": fuel_consumption,
                    "occupiedSeats": occupied_seats,
                    "origin": origin,
                    "destination": destination
                }
                try:
                    insert_flight(conn, new_flight)
                    st.success(f"Vuelo {new_flight_id} añadido correctamente.")
                except Exception as e:
                    st.error(f"Error al añadir vuelo: {e}")

def page_register_passenger_flight(conn):
    st.subheader("Registrar/actualizar pasajero en un vuelo")
    with st.form("form_register_passenger"):
        flight_id = st.text_input("ID de vuelo (flightId)")
        passenger_id = st.text_input("ID del pasajero (passengerId)")
        status_input = st.selectbox("Estado del pasajero en el vuelo", 
                                    ["Boarded", "Cancelled", "Checked-in", "No-show"])

        submitted_passenger = st.form_submit_button("Registrar/Actualizar")
        if submitted_passenger:
            if not flight_id or not passenger_id:
                st.error("Debe especificar flightId y passengerId.")
            else:
                try:
                    register_passenger_in_flight(conn, flight_id, passenger_id, status_input)
                    st.success(f"Pasajero {passenger_id} registrado/actualizado en el vuelo {flight_id}.")
                except Exception as e:
                    st.error(f"Error al registrar pasajero en vuelo: {e}")

def get_passengers(conn):
    '''Esta función lo que permite es ver a todos aquellos pasageros que han pasado por el aeropuerto'''
    query= '''
    SELECT * FROM passengers
    '''
    with conn.cursor() as cur: 
        cur.execute(query)
        rows= cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=columns)

def page_ver_passengers(conn): 
    '''Esto lo que nos permitiráa es ver en una página nueva toda la información sobre los pasajeros'''
    st.subheader('Ver Pasajeros ')
    try:
        df_passengers= get_passengers(conn)
        if not df_passengers.empty:
            st.dataframe(df_passengers)
        else:
            st.info('no se han encontrado pasageros')
    except Exception as e:
        st.error(f'error al obtener los datos {e}')

def get_maintenance(conn):
    '''Con esta parte pretendemos que nos muestre todos los aviones en el hangar y que nos diga el tiempo que le queda para que se realicen las maintenance''
    '''
    query = '''
    Select plateNumber, lastMaintenanceDate, nextMaintenanceDate, nextMaintenanceDate - NOW() as days_to_maintenance from airplanes
'''
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=columns)

def page_ver_maintenance(conn):
    '''Esto sirve para poder ver el tiempo que queda en streamlit'''
    st.subheader('Ver mantenimiento de aviones')
    try:
        df_maintenance = get_maintenance(conn)
        if not df_maintenance.empty:
            st.dataframe(df_maintenance)
        else:
            st.info('No se han encontrado aviones en mantenimiento')
    except Exception as e:
        st.error(f'Error al obtener los datos: {e}')

def main():
    st.title("Gestión de Aviones y Aeropuerto")
    
    # Intentamos la conexión a la base de datos
    try:
        conn = connect_to_postgres_rds()
    except Exception as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return

    # Menú lateral para navegar por las páginas
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox(
        "Selecciona la sección",
        (
            "Ver Aviones",
            "Añadir Avión",
            "Añadir Pasajero",
            "Añadir Vuelo",
            "Registrar/Actualizar Pasajero en Vuelo"
        )
    )

    # Lógica de navegación
    if page == "Ver Aviones":
        page_ver_aviones(conn)
    elif page == "Añadir Avión":
        page_add_airplane(conn)
    elif page == "Añadir Pasajero":
        page_add_passenger(conn)
    elif page == "Añadir Vuelo":
        page_add_flight(conn)
    elif page == "Registrar/Actualizar Pasajero en Vuelo":
        page_register_passenger_flight(conn)
    elif page == 'Ver Pasajeros':
        page_ver_passengers(conn)

    # Cerramos la conexión al final
    conn.close()

if __name__ == "__main__":
    main()

import logging
import os
import psycopg2
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

RDS_HOST = os.environ['RDS_HOST']
RDS_PORT = os.environ['RDS_PORT']
RDS_USER = os.environ['RDS_USER']
RDS_PASSWORD = os.environ['RDS_PASSWORD']
RDS_DB = os.environ['RDS_DB']

REDSHIFT_HOST = os.environ['REDSHIFT_HOST']
REDSHIFT_PORT = os.environ['REDSHIFT_PORT']
REDSHIFT_USER = os.environ['REDSHIFT_USER']
REDSHIFT_PASSWORD = os.environ['REDSHIFT_PASSWORD']
REDSHIFT_DB = os.environ['REDSHIFT_DB']


def connect_to_postgres_rds():
    return psycopg2.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB
    )


def connect_to_redshift():
    return psycopg2.connect(
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT,
        user=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD,
        database=REDSHIFT_DB
    )


def extract_data_from_postgres(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name};")
    data = cur.fetchall()
    cur.close()
    return data


def extract_schema_and_type_from_postgres(conn, table_name):
    cur = conn.cursor()
    cur.execute(f'''
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
    ''')
    schema = cur.fetchall()
    cur.close()
    return schema


def create_table_from_schema_in_aws_redshift(conn, schema, table_name):
    cur = conn.cursor()
    query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(f'{column[0]} {column[1]}' for column in schema)}
        );
    '''
    cur.execute(query)
    conn.commit()
    cur.close()


def insert_data_redshift(conn, data, schema, table_name):
    cur = conn.cursor()
    columns = ', '.join([column[0] for column in schema])
    placeholders = ', '.join(['%s' for _ in schema])
    query = f'''
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders});
    '''
    cur.execute(query, data)
    conn.commit()
    cur.close()


if __name__ == "__main__":
    postgres_tables = ['passengers', 'flight_passengers', 'flights', 'airplanes']

    logging.info("Connecting to databases")
    conn_postgres = connect_to_postgres_rds()
    conn_redshift = connect_to_redshift()
    logging.info("Connected to databases")

    for table in postgres_tables:
        logging.info(f"Processing table: {table}")

        # Extraer datos
        logging.info("Extracting data from PostgreSQL")
        data_rows = extract_data_from_postgres(conn_postgres, table)
        logging.info(f"Extracted {len(data_rows)} rows from {table}")

        # Extraer esquema
        logging.info("Extracting schema from PostgreSQL")
        schema = extract_schema_and_type_from_postgres(conn_postgres, table)
        logging.info(f"Extracted schema for {table}")

        # Crear tabla en Redshift
        logging.info("Creating table in Redshift")
        create_table_from_schema_in_aws_redshift(conn_redshift, schema, table)
        logging.info(f"Table {table} created in Redshift")

        # Insertar datos en Redshift
        logging.info("Inserting data into Redshift")
        for row in data_rows:
            insert_data_redshift(conn_redshift, row, schema, table)

        logging.info(f"Inserted data into {table}")

    conn_postgres.close()
    conn_redshift.close()
    logging.info("All connections closed")

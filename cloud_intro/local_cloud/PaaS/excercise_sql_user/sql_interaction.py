import logging
import os

import psycopg2

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


def create_connection(POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD,
                     POSTGRES_HOST, POSTGRES_PORT):
    try:
        connection = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )
        logger.info("Connected to the database!")
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def create_table(connection, cursor):
    cursor.execute("""
        CREATE TABLE cloud_providers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            year_created INTEGER
        );
    """)
    connection.commit()
    logger.info("Table 'cloud_providers' created successfully.")


def insert_values(connection, cursor):
    cursor.execute("""
        INSERT INTO cloud_providers (name, year_created)
        VALUES ('AWS', 2002), ('GCP', 2008), ('AZURE', 2010);
    """)
    connection.commit()
    logger.info("Data inserted successfully.")


def query_table(cursor):
    cursor.execute("SELECT * FROM cloud_providers;")
    rows = cursor.fetchall()
    return rows

def close_connection(connection, cursor):
    cursor.close()
    connection.close()
    logger.info("Connection closed.")


if __name__ == "__main__":
    # Connection details
    POSTGRES_HOST = "<DB_IP_ADDRESS>"
    POSTGRES_PORT = "5432"
    POSTGRES_USER = "<edem-user>"
    POSTGRES_PASSWORD = "<edem-password>"
    POSTGRES_DB = "<edem-db>"
    connection, cursor = create_connection(POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD,
                                          POSTGRES_HOST, POSTGRES_PORT)
    create_table(connection, cursor)
    insert_values(connection, cursor)
    table_rows = query_table(cursor)
    for row in table_rows:
        logger.info(row)
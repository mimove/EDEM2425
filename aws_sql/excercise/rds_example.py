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


def connect_to_postgres_rds() -> psycopg2.connect:
    conn = psycopg2.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB
    )
    return conn


def create_database(conn: psycopg2.connect) -> None:
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname='testdb';")
    exists = cur.fetchone()
    if not exists:
        cur.execute("CREATE DATABASE testdb;")


def create_table(conn: psycopg2.connect) -> None:
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS test_table_name (id serial PRIMARY KEY,
                name VARCHAR(50), created_at TIMESTAMP);""")


def insert_data(conn: psycopg2.connect, data: str) -> None:
    cur = conn.cursor()
    query = "INSERT INTO test_table_name (name, created_at) VALUES (%s, NOW());"
    cur.execute(query, (data,))
    conn.commit()


if __name__ == "__main__":
    logging.info("Connecting to RDS")
    conn = connect_to_postgres_rds()
    logging.info("Connected to RDS")
    logging.info("Creating database")
    create_database(conn)
    logging.info("Database created")
    logging.info("Creating table")
    create_table(conn)
    logging.info("Table created")
    logging.info("Inserting data")
    insert_data(conn, "jacinto")
    logging.info("Data inserted")
    conn.close()

import logging
import os
from datetime import datetime

import psycopg2
from clickhouse_driver import Client


class DbManager:
    def __init__(self, OLTP_DB_CONFIG, OLAP_DB_CONFIG):
        self.OLTP_DB_CONFIG = OLTP_DB_CONFIG
        self.OLAP_DB_CONFIG = OLAP_DB_CONFIG
        self.conn_oltp = None
        self.conn_olap = None

    def _connect_postgres(self):
        try:
            self.conn_oltp = psycopg2.connect(**self.OLTP_DB_CONFIG)
            logging.info("Connected to PostgreSQL successfully.")
            return self.conn_oltp.cursor()
        except Exception as e:
            logging.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    def _connect_clickhouse(self):
        try:
            self.conn_olap = Client(**self.OLAP_DB_CONFIG)
            logging.info("Connected to ClickHouse successfully.")
            return self.conn_olap
        except Exception as e:
            logging.error(f"Failed to connect to ClickHouse: {e}")
            raise

    def get_operational_data(self, table):
        try:
            cursor_oltp = self._connect_postgres()
            cursor_oltp.execute(f"SELECT * FROM {table}")
            data = cursor_oltp.fetchall()
            return data
        except Exception as e:
            logging.error(f"Error during customer synchronization: {e}")
        finally:
            if cursor_oltp:
                cursor_oltp.close()
                logging.info("Closed PostgreSQL connection.")

    def write_to_analytical_db(self, data, table, table_ddl, values):
        try:
            client_olap = self._connect_clickhouse()
            logging.info(f"Fetched {len(data)} {table} from PostgreSQL.")
            client_olap.execute(f"DROP TABLE IF EXISTS {table}_temp")
            client_olap.execute(table_ddl)
            logging.info(f"Created table {table}_temp in ClickHouse.")
            query = f"INSERT INTO analytics_db.{table}_temp VALUES {values}"
            client_olap.execute(query)
            logging.info(f"Inserted data into {table}_temp table.")
            client_olap.execute(f"""
                RENAME TABLE {table} TO {table}_old, {table}_temp TO {table}
            """)
            client_olap.execute(f"DROP TABLE IF EXISTS {table}_old")
            logging.info(f"Successfully synchronized {table}  table.")
        except Exception as e:
            logging.error(f"Error during customer synchronization: {e}")


def syncronize_customers(db_conn_manager, data):
    customers_ddl = """CREATE TABLE customers_temp (id UInt32, customer_name String,
                                                    email String)
                                                    ENGINE = MergeTree() ORDER BY id"""
    customer_values = ", ".join(
                f"({row[0]}, '{row[1]}', '{row[2]}')" for row in data
            )
    db_conn_manager.write_to_analytical_db(data, 'customers', customers_ddl,
                                           customer_values)


def syncronize_products(db_conn_manager, data):
    products_ddl = """CREATE TABLE products_temp (id UInt32, product_name String,
                                                  price Float32) ENGINE = MergeTree()
                                                  ORDER BY id"""
    products_value = ", ".join(
                f"""({row[0]}, '{row[1].replace("'", "")}', {row[2]})""" for row in data
            )
    db_conn_manager.write_to_analytical_db(data, 'products', products_ddl, products_value)


def syncronize_orders(db_conn_manager, data):
    orders_ddl = """CREATE TABLE orders_temp (id UInt32, customer_id UInt32,
                                              created_at DateTime, total_price Float32)
                                              ENGINE = MergeTree() ORDER BY id """
    orders_value = ", ".join(
                f"""({row[0]}, {row[1]}, '{row[2].strftime('%Y-%m-%d %H:%M:%S')}',
                     {row[3]})""" for row in data
            )
    db_conn_manager.write_to_analytical_db(data, 'orders', orders_ddl, orders_value)


def syncronize_order_products(db_conn_manager, data):
    order_products_ddl = """CREATE TABLE order_products_temp
                            (order_id UInt32, product_id UInt32, quantity UInt32, 
                             price Float32) ENGINE = MergeTree()
                             ORDER BY (order_id, product_id)"""
    order_products_value = ", ".join(
                f"""({row[0]}, {row[1]}, {row[2]}, {row[3]})""" for row in data
            )
    db_conn_manager.write_to_analytical_db(data, 'order_products', order_products_ddl,
                                           order_products_value)


if __name__ == "__main__":
    logging.basicConfig(
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.StreamHandler()
                        ]
    )
    logger = logging.getLogger()
    OLTP_DB_CONFIG = {
        "dbname": "ecommerce",
        "user": "user",
        "password": "password",
        "host": os.getenv('HOST_IP'),
        "port": 5432,
    }
    OLAP_DB_CONFIG = {
        "host": "localhost",
        "port": 9001,
        "database": "analytics_db",
        "user": "user",
        "password": "password",
        "send_receive_timeout": 10
    }
    logging.info("Starting syncronization.")
    db_conn_manager = DbManager(OLTP_DB_CONFIG, OLAP_DB_CONFIG)

    customers = db_conn_manager.get_operational_data('customers')
    syncronize_customers(db_conn_manager, customers)

    products = db_conn_manager.get_operational_data('products')
    syncronize_products(db_conn_manager, products)

    orders = db_conn_manager.get_operational_data('orders')
    syncronize_orders(db_conn_manager, orders)

    order_products = db_conn_manager.get_operational_data('order_products')
    syncronize_order_products(db_conn_manager, order_products)
    logging.info("Synchronization completed.")

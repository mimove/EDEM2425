import os
from datetime import datetime

import psycopg2
from clickhouse_driver import Client

# Database configuration
OLTP_DB_CONFIG = {
    "dbname": "ecommerce",
    "user": "user",
    "password": "password",
    "host": os.getenv('HOST_IP'),  # Change to the OLTP DB host
    "port": 5432,
}

OLAP_DB_CONFIG = {
    "host": "localhost",  # Change to the OLAP DB host
    "port": 8124,
    "database": "analytics_db",  # Set to your OLAP database name
    "user": "user",
    "password": "password",
    "send_receive_timeout": 120
}

def sync_data():
    """Synchronize tables from OLTP to OLAP without downtime."""
    # try:
    # Connect to OLTP and OLAP databases
    conn_oltp = psycopg2.connect(**OLTP_DB_CONFIG)
    print('Connection to operational_db successful')
    cursor_oltp = conn_oltp.cursor()
    client_olap = Client(**OLAP_DB_CONFIG)
    print('Connection to analytical_db successful')

    # Replace customers
    cursor_oltp.execute("SELECT * FROM customers")
    customers = cursor_oltp.fetchall()
    client_olap.execute("DROP TABLE IF EXISTS customers_temp")
    print('droping table')
    client_olap.execute("""
        CREATE TABLE customers_temp (
            id UInt32,
            customer_name String,
            email String
        ) ENGINE = MergeTree() ORDER BY id
    """)
    print('customers_temp created')
    client_olap.execute(
        "INSERT INTO customers_temp (id, name, email) VALUES", customers
    )
    print('customers_temp populated')
    client_olap.execute("RENAME TABLE customers TO customers_old, customers_temp TO customers")
    client_olap.execute("DROP TABLE IF EXISTS customers_old")
    print(f"Synchronized {len(customers)} customers.")

    # Replace products
    cursor_oltp.execute("SELECT id, name, price FROM products")
    products = cursor_oltp.fetchall()
    client_olap.execute("DROP TABLE IF EXISTS products_temp")
    client_olap.execute("""
        CREATE TABLE products_temp (
            id UInt32,
            product_name String,
            price Float32
        ) ENGINE = MergeTree() ORDER BY id
    """)
    client_olap.execute(
        "INSERT INTO products_temp (id, name, price) VALUES", products
    )
    client_olap.execute("RENAME TABLE products TO products_old, products_temp TO products")
    client_olap.execute("DROP TABLE IF EXISTS products_old")
    print(f"Synchronized {len(products)} products.")

    # Replace orders
    cursor_oltp.execute("SELECT id, customer_id, timestamp, total_price FROM orders")
    orders = cursor_oltp.fetchall()
    client_olap.execute("DROP TABLE IF EXISTS orders_temp")
    client_olap.execute("""
        CREATE TABLE orders_temp (
            id UInt32,
            customer_id UInt32,
            created_at DateTime,
            total_price Float32
        ) ENGINE = MergeTree() ORDER BY id
    """)
    client_olap.execute(
        "INSERT INTO orders_temp (id, customer_id, created_at, total_price) VALUES", orders
    )
    client_olap.execute("RENAME TABLE orders TO orders_old, orders_temp TO orders")
    client_olap.execute("DROP TABLE IF EXISTS orders_old")
    print(f"Synchronized {len(orders)} orders.")

    # Replace order_products
    cursor_oltp.execute("SELECT order_id, product_id, quantity, price FROM order_products")
    order_products = cursor_oltp.fetchall()
    client_olap.execute("DROP TABLE IF EXISTS order_products_temp")
    client_olap.execute("""
        CREATE TABLE order_products_temp (
            order_id UInt32,
            product_id UInt32,
            quantity UInt32,
            price Float32
        ) ENGINE = MergeTree() ORDER BY (order_id, product_id)
    """)
    client_olap.execute(
        "INSERT INTO order_products_temp (order_id, product_id, quantity, price) VALUES",
        order_products
    )
    client_olap.execute("RENAME TABLE order_products TO order_products_old, order_products_temp TO order_products")
    client_olap.execute("DROP TABLE IF EXISTS order_products_old")
    print(f"Synchronized {len(order_products)} order-product relationships.")

    print(f"Synchronization completed at {datetime.now()}.")

    # except Exception as e:
    #     print(f"Error during synchronization: {e}")

    # finally:
    #     cursor_oltp.close()
    #     conn_oltp.close()

if __name__ == "__main__":
    sync_data()

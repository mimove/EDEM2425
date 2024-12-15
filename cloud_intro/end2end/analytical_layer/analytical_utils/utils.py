import json
import logging
import os
import sys

import psycopg2
from clickhouse_driver import Client

from kafka import KafkaConsumer, errors


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

    def write_tables_to_analytical_db(self, data, table, table_ddl, values):
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

    def write_events_to_analytical_db(self, data, table, values):
        try:
            client_olap = self._connect_clickhouse()
            logging.info(f"Fetched {len(data)} {table} from Kafka.")
            query = f"INSERT INTO analytics_db.{table} VALUES {values}"
            client_olap.execute(query)
            logging.info(f"Successfully synchronized {table}  table.")
        except Exception as e:
            logging.error(f"Error during customer synchronization: {e}")


class DeliveryEventsManager:
    def __init__(self, topic_name):
        self.topic_name = topic_name

    def create_consumer(self, group_id='default-group', auto_offset_reset='earliest',
                        enable_auto_commit=True):
        logging.info("Connecting to Kafka Consumer")
        KAFKA_IP = os.getenv('KAFKA_IP')
        try:
            self.consumer = KafkaConsumer(
                self.topic_name,
                bootstrap_servers=f'{KAFKA_IP}:9092',
                group_id=group_id,
                auto_offset_reset=auto_offset_reset,
                enable_auto_commit=enable_auto_commit,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                consumer_timeout_ms=5000
            )
            logging.info('Kafka consumer connected successfully')
        except errors.NoBrokersAvailable as err:
            logging.error(f"Failed to connect to Kafka Consumer: {err}")
            sys.exit(1)

    def consume_messages(self):
        logging.info('Consuming messages...')
        if not self.consumer:
            logging.error("Consumer is not initialized. Call create_consumer() first.")
            return
        empty_poll_count = 0
        try:
            while True:
                messages = self.consumer.poll(timeout_ms=1000)
                if not messages:
                    empty_poll_count += 1
                    if empty_poll_count >= 2:
                        logging.info("No more messages to consume. Exiting.")
                        break
                else:
                    empty_poll_count = 0
                    for _, msg_list in messages.items():
                        for message in msg_list:
                            logging.info(f"Consumed message: {message.value}")
                            yield message.value
        except Exception as err:
            logging.error(f"Error while consuming messages: {err}")
        finally:
            if self.consumer:
                self.consumer.close()
                logging.info("Kafka consumer closed.")

import logging
import json
import os
import sys

from kafka import KafkaProducer, KafkaConsumer, errors


class EventsManager:
    def __init__(self, topic_name):
        self.payload = {}
        self.topic_name = topic_name
        self.producer = None
        self.consumer = None

    def create_producer(self):
        logging.info("Connecting to Kafka Producer")
        KAFKA_IP = os.getenv('KAFKA_IP')
        try:
            self.producer = KafkaProducer(bootstrap_servers=f'{KAFKA_IP}:9092',
                                          value_serializer=lambda v: json.dumps(v).
                                          encode('utf-8'))
            logging.info('Kafka producer connected succesfully')
        except errors.NoBrokersAvailable as err:
            logging.error(f"Failed to connect to Kafka Producer: {err}")
            sys.exit(1)

    def send_message(self, message):
        logging.info('Sending messages...')
        try:
            self.producer.send(self.topic_name, message)
            self.producer.flush()
            logging.info('Message sent correctly')
        except ValueError as err:
            logging.err(f"Couldn't send message {message} due to {err}")

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
                value_deserializer=lambda v: json.loads(v.decode('utf-8'))
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
        try:
            for message in self.consumer:
                logging.info(f"Consumed message: {message.value}")
                yield message.value
        except Exception as err:
            logging.error(f"Error while consuming messages: {err}")

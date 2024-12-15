import logging
import json
import os
import sys

from kafka import KafkaProducer, errors


class EventsManager:
    def __init__(self, topic_name):
        self.payload = {}
        self.topic_name = topic_name
        self.producer = None

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

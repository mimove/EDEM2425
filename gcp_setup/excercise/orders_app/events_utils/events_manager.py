import logging
import json
import os
import sys
import google.auth

from confluent_kafka import Producer


class EventsManager:
    def __init__(self, topic_name):
        self.payload = {}
        self.topic_name = topic_name
        self.producer = None
    
    def _make_token(args):
        credentials, _project = google.auth.default()
        credentials.refresh()
        return credentials.token

    def create_producer(self):
        logging.info("Connecting to Kafka Producer")
        KAFKA_IP = os.getenv('KAFKA_IP')
        try:
            config = {
                        'bootstrap.servers': f'{KAFKA_IP}:9092',
                        'security.protocol': 'SASL_SSL',
                        'sasl.mechanisms': 'OAUTHBEARER',
                        'oauth_cb': self._make_token,
                    }
            self.producer = Producer(config)
            logging.info('Kafka producer connected succesfully')
        except ValueError as err:
            logging.error(f"Failed to connect to Kafka Producer: {err}")
            sys.exit(1)

    def send_message(self, message):
        logging.info('Sending messages...')
        try:
            serialized_data = json.dumps(message).encode('utf-8')
            self.producer.produce(self.topic_name, serialized_data)
            self.producer.flush()
            logging.info('Message sent correctly')
        except ValueError as err:
            logging.err(f"Couldn't send message {message} due to {err}")

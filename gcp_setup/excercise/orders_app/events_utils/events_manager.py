import logging
import json
import os
import sys


from google.cloud import pubsub_v1


class EventsManager:
    def __init__(self, topic_path):
        self.payload = {}
        self.topic_path = topic_path
        self.producer = None
    

    def create_producer(self):
        logging.info("Connecting to PubSub Producer")
        GOOGLE_CLOUD_PROJECT = os.getenv('project_id')
        try:
            self.producer = pubsub_v1.PublisherClient(GOOGLE_CLOUD_PROJECT, self.topic_path)
            logging.info('PubSub producer connected succesfully')
        except ValueError as err:
            logging.error(f"Failed to connect to PubSub Producer: {err}")
            sys.exit(1)

    def send_message(self, message):
        logging.info('Sending messages...')
        try:
            serialized_data = json.dumps(message).encode('utf-8')
            self.producer.publish(self.topic_path, serialized_data)
            logging.info('Message sent correctly')
        except ValueError as err:
            logging.err(f"Couldn't send message {message} due to {err}")

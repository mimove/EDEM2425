import base64
import datetime
import logging
import json
import os
import sys

from google.cloud import pubsub_v1

class EventsManager:
    def __init__(self, topic_name):
        self.payload = {}
        self.topic_name = topic_name
        self.publisher = None
        self.topic_path = None
        self.subscriber = None
        self.subscriber_path = None
    
    def create_producer(self):
        logging.info("Connecting to Kafka Producer")
        PROJECT_ID = os.getenv('PROJECT_ID')
        try:
            self.publisher = pubsub_v1.PublisherClient()
            self.topic_path = self.publisher.topic_path(PROJECT_ID, self.topic_name)
            logging.info('PubSub publisher connected succesfully')
        except ValueError as err:
            logging.error(f"Failed to connect to PubSub Publisher: {err}")
            sys.exit(1)

    def send_message(self, message):
        logging.info('Sending messages...')
        try:
            serialized_data = json.dumps(message).encode('utf-8')
            self.publisher.publish(self.topic_path, serialized_data)
            logging.info('Message sent correctly')
        except ValueError as err:
            logging.err(f"Couldn't send message {message} due to {err}")

    def create_subscriber(self, subscription_name):
        logging.info("Connecting to PubSub Subscriptor")
        PROJECT_ID = os.getenv('PROJECT_ID')
        try:
            self.subscriber = pubsub_v1.SubscriberClient()
            self.subscriber_path = self.subscriber.subscription_path(PROJECT_ID,
                                                                   subscription_name)
            logging.info('PubSub subscriber connected successfully')
        except ValueError as err:
            logging.error(f"Failed to connect to PubSub Subscriber: {err}")
            sys.exit(1)
      
    def consume_messages(self):
        logging.info('Consuming messages...')
        if not self.subscriber:
            logging.error("Subscriber is not initialized. Call create_subscriber() first.")
            return
        try:
            response = self.subscriber.pull(self.subscriber_path, max_messages=10)
            for received_message in response.received_messages:
                self.subscriber.acknowledge(self.subscriber_path, [message.ack_id])
                logging.info(f"Consumed message: {received_message.message.data.\
                                                  decode('utf-8')}")
                yield json.loads(received_message.message.data.decode('utf-8'))
        except Exception as err:
            logging.error(f"Couldn't consume message due to {err}")
        except KeyboardInterrupt:
            logging.info("Interrupted by user")
        finally:
            self.consumer.close()
            logging.info("Consumer closed")

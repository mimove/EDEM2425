import base64
import datetime
import logging
import json
import os
import sys
import time

import google.auth
import google.auth.transport.urllib3
import urllib3
from confluent_kafka import Producer

class TokenProvider(object):

  def __init__(self, **config):
    self.credentials, _project = google.auth.default()
    self.http_client = urllib3.PoolManager()
    self.HEADER = json.dumps(dict(typ='JWT', alg='GOOG_OAUTH2_TOKEN'))

  def valid_credentials(self):
    if not self.credentials.valid:
      self.credentials.refresh(google.auth.transport.urllib3.Request(self.http_client))
    return self.credentials

  def get_jwt(self, creds):
    return json.dumps(
        dict(
            exp=creds.expiry.timestamp(),
            iss='Google',
            iat=datetime.datetime.now(datetime.timezone.utc).timestamp(),
            scope='kafka',
            sub=creds.service_account_email,
        )
    )

  def b64_encode(self, source):
    return (
        base64.urlsafe_b64encode(source.encode('utf-8'))
        .decode('utf-8')
        .rstrip('=')
    )

  def get_kafka_access_token(self, creds):
    return '.'.join([
      self.b64_encode(self.HEADER),
      self.b64_encode(self.get_jwt(creds)),
      self.b64_encode(creds.token)
    ])

  def token(self):
    creds = self.valid_credentials()
    return self.get_kafka_access_token(creds)

  def confluent_token(self):
    creds = self.valid_credentials()

    utc_expiry = creds.expiry.replace(tzinfo=datetime.timezone.utc)
    expiry_seconds = (utc_expiry - datetime.datetime.now(datetime.timezone.utc)).total_seconds()

    return self.get_kafka_access_token(creds), time.time() + expiry_seconds

class EventsManager:
    def __init__(self, topic_name):
        self.payload = {}
        self.topic_name = topic_name
        self.producer = None
    
    def _make_token(args):
        """Method to get the Token"""
        t = TokenProvider()
        token = t.confluent_token()
        print("Generated Token:", token)
        return token


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

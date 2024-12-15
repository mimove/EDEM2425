import logging
import requests
from utils.events_manager import EventsManager


if __name__ == "__main__":
    logging.basicConfig(
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.StreamHandler()
                        ]
    )
    logger = logging.getLogger()
    producer = EventsManager('events-ecommerce-mimove')
    producer.create_producer()
    messages = [{'name': 'test1', 'id': 1}, {'name': 'test2', 'id': 2}]
    for message in messages:
        producer.send_message(message)

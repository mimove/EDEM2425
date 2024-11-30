import logging
import os

import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


def create_database(API_BASE_URL, db_name):
    db_data = {
        "dbname": db_name
    }
    response = requests.post(f"{API_BASE_URL}/create_database", json=db_data)
    logging.info(f"Create Database Response: {response.json()}")


def create_user(API_BASE_URL, username, password):
    user_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{API_BASE_URL}/create_user", json=user_data)
    logging.info(f"Create User Response: {response.json()}")


if __name__ == "__main__":
    DB_IP_ADDRESS = os.getenv("DB_IP_ADDRESS")
    API_BASE_URL = f"http://{DB_IP_ADDRESS}:5000"

    db_name = "<edem-user>_db"
    username = "<edem-user>"
    password = "<your-password>"

    create_database(API_BASE_URL, db_name)
    create_user(API_BASE_URL, username, password)

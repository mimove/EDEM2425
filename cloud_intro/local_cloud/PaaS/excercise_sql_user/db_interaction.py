import os
import requests

DB_IP_ADDRESS = os.getenv("DB_IP_ADDRESS")

API_BASE_URL = f"http://{DB_IP_ADDRESS}:5000"

# Create a database
db_data = {
    "dbname": "<edem-username>_db"
}
response = requests.post(f"{API_BASE_URL}/create_database", json=db_data)
print("Create Database Response:", response.json())

# Create a user
user_data = {
    "username": "<edem-username>",
    "password": "<your-password>"
}
response = requests.post(f"{API_BASE_URL}/create_user", json=user_data)
print("Create User Response:", response.json())

import serial
import json
import os
import datetime
from google.cloud import pubsub_v1

# Google Cloud Configuration
PROJECT_ID = "edem-24-25-mimove"
TOPIC_ID = "edem-iot-pubsub"

# Set credentials explicitly for Pub/Sub (Project edem-24-25-mimove)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize Pub/Sub Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

# Serial Configuration
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyACM0")
BAUD_RATE = 115200

try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"Listening on {SERIAL_PORT} and publishing to Pub/Sub topic '{TOPIC_ID}'...")

        while True:
            line = ser.readline().decode("utf-8").strip()
            if line:
                try:
                    data = json.loads(line)  # Parse JSON from Serial

                    data["sent_at"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

                    print(json.dumps(data, indent=2)) 

                    # Encode and publish message to Pub/Sub
                    message = json.dumps(data).encode("utf-8")
                    future = publisher.publish(topic_path, message)

                    print(f"Published message ID: {future.result()}")

                except json.JSONDecodeError:
                    print(f"Error: Received malformed JSON: {line}")

except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("\nExiting...")

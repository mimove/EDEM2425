import json
import time
import os
from google.cloud import pubsub_v1, bigtable

# Google Cloud Configuration
PUBSUB_PROJECT_ID = "edem-24-25-mimove"  # Project where the Pub/Sub topic is
BIGTABLE_PROJECT_ID = "<your-project-id>"  # Project where Bigtable is
TOPIC_ID = "edem-iot-pubsub"
SUBSCRIPTION_ID = "<edem-user>-subscription"
BIGTABLE_INSTANCE_ID = "edem-bigtable-iot"
BIGTABLE_TABLE_ID = "sensors_data"

# Set credentials explicitly for Pub/Sub (Project edem-24-25-mimove)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PUBSUB")
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

# Define paths
subscription_path = subscriber.subscription_path(PUBSUB_PROJECT_ID, SUBSCRIPTION_ID)
topic_path = publisher.topic_path(PUBSUB_PROJECT_ID, TOPIC_ID)

# Set credentials explicitly for Bigtable
bigtable_client = bigtable.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_BIGTABLE"), project=BIGTABLE_PROJECT_ID)
instance = bigtable_client.instance(BIGTABLE_INSTANCE_ID)
table = instance.table(BIGTABLE_TABLE_ID)

# Function to create Pub/Sub subscription if it doesn't exist
def ensure_subscription_exists():
    try:
        # Check if subscription exists
        subscriptions = list(subscriber.list_subscriptions(request={"project": f"projects/{PUBSUB_PROJECT_ID}"}))
        existing_subscriptions = [sub.name for sub in subscriptions]

        if subscription_path not in existing_subscriptions:
            print(f"Subscription {SUBSCRIPTION_ID} not found. Creating...")
            subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
            print(f"Subscription {SUBSCRIPTION_ID} created successfully.")
        else:
            print(f"Subscription {SUBSCRIPTION_ID} already exists.")
    except Exception as e:
        print(f"Error checking/creating subscription: {e}")

# Function to process incoming Pub/Sub messages
def callback(message):
    try:
        # Parse message data
        event_data = json.loads(message.data.decode("utf-8"))
        temperature = event_data.get("temperature")
        led = event_data.get("led")
        sensor_id = event_data.get("id")
        sent_at = event_data.get("sent_at", time.strftime("%Y-%m-%dT%H:%M:%S"))

        print(f"Received message: {event_data}")

        # Create Bigtable row key (using timestamp)
        row_key = f"{int(time.time() * 1000)}".encode("utf-8")
        row = table.direct_row(row_key)

        # Write to 'measures' column family
        row.set_cell("measures", "temperature", str(temperature).encode("utf-8"))
        row.set_cell("measures", "led", str(led).encode("utf-8"))
        row.set_cell("measures", "sent_at", sent_at.encode("utf-8"))  # Store sent_at timestamp

        # Write to 'identification' column family
        row.set_cell("identification", "sensor_id", str(sensor_id).encode("utf-8"))

        # Commit row
        row.commit()
        print(f"Inserted row {row_key.decode('utf-8')} into Bigtable with sent_at: {sent_at}")

        # Acknowledge the message
        message.ack()

    except Exception as e:
        print(f"Error processing message: {e}")

# Ensure subscription exists and start listening
def main():
    ensure_subscription_exists()
    print(f"Listening for messages on {SUBSCRIPTION_ID} from {PUBSUB_PROJECT_ID} and writing to Bigtable in {BIGTABLE_PROJECT_ID}...")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        print("\nSubscription stopped.")

if __name__ == "__main__":
    main()

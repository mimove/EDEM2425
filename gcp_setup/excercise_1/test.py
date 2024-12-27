from google.cloud import pubsub_v1

project_id = "your-project-id"
topic_id = "your-topic-id"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_message(data):
    data = data.encode("utf-8")  # Data must be a bytestring
    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

# Example usage
publish_message("Hello, Pub/Sub!")

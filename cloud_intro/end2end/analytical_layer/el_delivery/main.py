import logging

from analytical_utils.utils import DeliveryEventsManager, DbManager


def get_delivery_messages(message):
    delivery_messages = []
    try:
        if not isinstance(message, dict) or 'order_id' not in message:
            logger.warning(f"Invalid message format: {message}")
        delivery_messages.append(message)
        logger.info(f"Storing delivery message: {message}")
        return delivery_messages
    except Exception as message_error:
        logger.error(f"Error processing message {message}: {message_error}")
        raise


if __name__ == "__main__":
    logging.basicConfig(
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.StreamHandler()
                        ]
    )
    logger = logging.getLogger()
    delivery_message_consumer = DeliveryEventsManager('delivery-events')
    delivery_message_consumer.create_consumer(group_id='mimove-consumer')
    all_events = []
    for message in delivery_message_consumer.consume_messages():
        delivery_event = get_delivery_messages(message)
        all_events.append(delivery_event)
        if len(all_events) == 10:
            print(all_events)
            all_events = []

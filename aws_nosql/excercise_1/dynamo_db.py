import logging

import boto3

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s - %(levelname)s')


def create_table(table_example):
    if table_example in [table.name for table in dynamodb.tables.all()]:
        logging.info("Table already exists")
        return
    table = dynamodb.create_table(
        TableName=table_example,
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},  # Partition key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.wait_until_exists()
    logging.info(f"Table status: {table.table_status}")


def put_item(user_id, name, table_example):
    table = dynamodb.Table(table_example)
    table.put_item(
        Item={
            'user_id': user_id,
            'name': name
        }
    )
    logging.info(f"Added user: {user_id} - {name}")


def get_item(user_id, table_example):
    table = dynamodb.Table(table_example)
    response = table.get_item(Key={'user_id': user_id})
    item = response.get('Item')
    logging.info(f"Retrieved item: {item}")


def update_item(user_id, new_name, table_example):
    table = dynamodb.Table(table_example)
    table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET #n = :name',
        ExpressionAttributeValues={':name': new_name},
        ExpressionAttributeNames={'#n': 'name'}
    )
    logging.info(f"Updated user {user_id} to {new_name}")


def delete_item(user_id, table_example):
    table = dynamodb.Table(table_example)
    table.delete_item(Key={'user_id': user_id})
    logging.info(f"Deleted user: {user_id}")


if __name__ == "__main__":
    table_name = 'Users'
    logging.info("Creating table")
    create_table(table_example=table_name)
    logging.info("Table created")
    input("Press Enter to insert item...")
    logging.info("Adding one item")
    put_item('1', 'Alice', table_example=table_name)
    logging.info("Item added")
    input("Press Enter to get item...")
    logging.info("Getting item")
    get_item('1', table_example=table_name)
    logging.info("Got item")
    input("Press Enter to update item...")
    logging.info("Updating item")
    update_item('1', 'Alice Smith', table_example=table_name)
    logging.info("Item updated")
    input("Press Enter to delete item...")
    logging.info("Deleting item")
    delete_item('1', table_example=table_name)
    logging.info("Item deleted")
    logging.info("All done!")
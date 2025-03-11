# AWS DynamoDB Exercises

# Excercise 1

This exercise demonstrates basic CRUD operations with Amazon DynamoDB using the AWS SDK for Python (boto3).

## Overview

The dynamo_db.py script demonstrates the following operations:

1. Creating a DynamoDB table
2. Adding items to the table
3. Retrieving items by primary key
4. Updating existing items
5. Deleting items

## Prerequisites
- virtual environment (`python3 -m venv venv`)
- boto3 library installed (`pip install boto3`)

## Code Explanation

The script uses the following core functions:

- `create_table()`: Creates a "Users" table with "user_id" as the partition key
- `put_item()`: Adds a new user to the table
- `get_item()`: Retrieves a user by their ID
- `update_item()`: Updates a user's name
- `delete_item()`: Deletes a user from the table

## How to Run

Simply execute the script to run through all operations in sequence:

```python
python dynamo_db.py
```


# Excercise 2

## Introduction

The scripts has been created using the example in the following [link](https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html)

The excercise demonstrates the following operations:

1. Creating a DynamoDB table
2. Adding items to the table
3. Retrieving items by primary key
4. Updating existing items
5. Deleting items
6. Querying items


from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import (
    IntegerType,
    StringType,
    TimestampType,
    NestedField,
)
from pyiceberg.partitioning import PartitionSpec

# Load the Iceberg catalog
catalog = load_catalog(
    "glue",
    **{
        "type": "glue",
        "warehouse": "s3://mimove-edem/",  # Replace with your S3 bucket
        "region": "eu-north-1",
    }
)

# Define the table schema
schema = Schema(
    NestedField(field_id=1, name="id", field_type=IntegerType(), required=True),
    NestedField(field_id=2, name="name", field_type=StringType(), required=False),
    NestedField(field_id=3, name="created_at", field_type=TimestampType(), required=False),
)

# Define the partition spec (optional)
partition_spec = PartitionSpec(spec_id=0)

# Table name and location
table_name = "db1.example_table"
table_location = "s3://mimove-edem/db1/example_table"  # Replace with your desired location

# Create the table
catalog.create_table(
    identifier=table_name,
    location=table_location,
    schema=schema,
    partition_spec=partition_spec,
)

print(f"Table '{table_name}' created successfully!")
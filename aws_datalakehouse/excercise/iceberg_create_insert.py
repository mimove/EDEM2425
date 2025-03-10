import logging

import numpy as np
import pandas as pd
from pyarrow import Table
from pyiceberg.catalog import Catalog, load_catalog
from pyiceberg.partitioning import PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.types import (
    IntegerType,
    NestedField,
    StringType,
    TimestampType,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_catalog_iceberg(provider: str, warehouse_bucket: str, region: str) -> Catalog:
    return load_catalog(
        provider,
        **{
            "type": provider,
            "warehouse": warehouse_bucket,
            "region": region,
        }
    )


def create_table_iceberg(catalog: Catalog, schema: dict, table_name: str,
                         table_location: str, partition_spec: str) -> None:
    if catalog.table_exists(table_name):
        logging.info(f"Table '{table_name}' already exists!")
        return None
    catalog.create_table(
        identifier=table_name,
        location=table_location,
        schema=schema,
        partition_spec=partition_spec,
    )


def insert_data_iceberg(data: dict,
                        iceberg_table: Table) -> None:
    df = pd.DataFrame(data)
    arrow_table = Table.from_pandas(df)
    with iceberg_table.transaction() as txn:
        txn.append(arrow_table)


def read_data_iceberg(table: Table) -> pd.DataFrame:
    rows = table.scan().to_arrow().to_pandas()
    return rows


if __name__ == "__main__":
    provider = "glue"
    warehouse_bucket = "s3://<your-bucket-name>/"
    region = "eu-north-1"
    catalog = load_catalog_iceberg(provider, warehouse_bucket, region)
    logging.info("Catalog loaded")

    database_name = "db1"
    table_name = "example_table"
    iceberg_table_identifier = f"{database_name}.{table_name}"
    schema = Schema(
        NestedField(field_id=1, name="id", field_type=IntegerType(), required=False),
        NestedField(field_id=2, name="name", field_type=StringType(), required=False),
        NestedField(field_id=3, name="created_at", field_type=TimestampType(),
                    required=False),
    )
    partition_spec = PartitionSpec(spec_id=0)
    iceberg_table_location = f"{warehouse_bucket}{database_name}/{table_name}"
    create_table_iceberg(catalog, schema, iceberg_table_identifier,
                                         iceberg_table_location, partition_spec)
    logging.info("Table created")

    data = {
    "id": pd.Series([1], dtype="Int32"),
    "name": ["jacinto"],
    "created_at": np.array(['2024-01-01 12:00:00'], dtype='datetime64[us]')
    }
    iceberg_table = catalog.load_table(iceberg_table_identifier)
    insert_data_iceberg(data, iceberg_table)
    logging.info("Data inserted")

    rows = read_data_iceberg(iceberg_table)
    logging.info(rows)

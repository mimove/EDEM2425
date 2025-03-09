import pandas as pd
from pyarrow import Table
from pyiceberg.catalog import load_catalog

catalog = load_catalog(
    "glue",
    **{
        "type": "glue",
        "warehouse": "s3:/<your-bucket>/",
        "region": "eu-north-1",
    }
)

data = {
    "id": [2],
    "name": ["jacinto"],
    "created_at": [pd.Timestamp('2024-01-01 12:00:00')]
}

table_name = "db1.table1"
table = catalog.load_table(table_name)

df = pd.DataFrame(data)

df["id"] = df["id"].astype("int32")

df["created_at"] = df["created_at"].astype("datetime64[us]")

arrow_table = Table.from_pandas(df)

with table.transaction() as txn:
    txn.append(arrow_table)

rows = table.scan().to_arrow().to_pandas()
print(rows)

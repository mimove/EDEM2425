# Inserting Sample Data

In this module we will learn how to insert sample data into the data lakehouse. We will use first AWS Athena to insert, merge and delete data and check how the different layers of Iceberg work.

**Prerequisites**
1. Configure AWS Athena. To do that, open AWS Athena.
2. At the top you'll see a message saying that before using athenea you need to configure a query result location in S3.
3. Go to S3 and create a new bucket with the name `athena-query-results-<edem-user>`.


## Inserting Data

Run the following query

```sql
INSERT INTO "example-1"."table-example"
VALUES (1, 'jacinto', timestamp '2023-01-01 12:00:00');
```

Go to the bucket where you stored the data and check the following. You should have two folders

- `data` where the data is stored. A parquet file will have been created with the data you inserted.
- `metadata` where the metadata is stored. You will see a folder with the name of the table and a file with the metadata of the table.

Download all the files from data and metadata.


## Mergint into/Upserting Data

Run the following query

```sql
MERGE INTO "example-1"."table-example" AS t
USING ( 
    SELECT 1 AS id, 'jacinto' AS name, timestamp '2023-01-01 13:00:00' AS created_at
    UNION ALL
    SELECT 2, 'pablo', timestamp '2023-01-01 13:00:00'
) AS s (id, name, created_at)
ON t.id = s.id
WHEN MATCHED THEN
    UPDATE SET created_at = s.created_at
WHEN NOT MATCHED THEN
    INSERT (id, name, created_at) VALUES (s.id, s.name, s.created_at);
```

Download the new files from data and metadata.


## Time Travel

Run the following query

```sql
SELECT * FROM "example-1"."table-example" 
FOR TIMESTAMP AS OF TIMESTAMP <timestamp for example '2023-01-01 12:00:00.000 UTC'>;
```

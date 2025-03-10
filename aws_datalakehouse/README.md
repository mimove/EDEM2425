# Excercises Data Lakehouse

## Introduction

In this module we will learn how to configure AWS S3 and AWS Glue to create a data lakehouse. We will also learn how to use AWS Glue to create a data catalog and how to use AWS Athena to query the data in the data lakehouse.

## Configuration of AWS S3

The steps to configure AWS S3 are as follows:

1. Go to the AWS Management Console and open the S3 console.
2. Click on the "Create bucket" button.
3. Enter a unique bucket name.
4. Select the region where you want to create the bucket.
5. Leave the rest of the settings as default.
6. Click on the "Create bucket" button.


## Configuration of AWS Glue

The steps to configure AWS Glue are as follows:

1. Go to the AWS Management Console and open the Glue console.
2. Click on the "Add database" button.
3. Enter a unique name for the database. For example `db1`.
4. Click on the "Create" button.
5. Click on the "Tables" tab.
6. Click on the "Add tables" button.
7. Enter `table1` as the table name.
8. In the Table Format section, select `Apache Iceberg table`.
9. Under table optimization remove the Compaction, snapshot retention and orpahn file deletion.
10. In table location, enter the S3 path where you want to store the data.
11. Click `Next`.
12. In the schema section, enter edit schema as JSON. Copy and paste the schema
```json
[
    {
      "Name": "id",
      "Type": "int"
    },
    {
      "Name": "name",
      "Type": "string"
    },
    {
      "Name": "created_at",
      "Type": "timestamp"
    }
  ]
```
13. Click `Next`.
14. Click `Create`.


**Useful Note**

To create a table using SQL in Iceberg format, you can run on Athena the following query:

```sql
CREATE TABLE <database>.<table_name> (
  id int,
  name string,
  created_at timestamp) 
PARTITIONED BY (created_at) 
LOCATION 's3://<bucket>' 
TBLPROPERTIES (
  'table_type'='ICEBERG',
  'format'='parquet'
)
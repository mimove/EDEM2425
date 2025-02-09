# Cloud Introduction and Storage

The following repo contains excercises related to the 2024-2025 Cloud introduction and storage modules of the Big Data & Cloud Master at EDEM

The folders are structured as follows:

**[cloud-intro](./cloud_intro/)**
- [local_cloud](./cloud_intro/local_cloud/): Use of VirtualBox to simulate locally IaaS and PaaS solutions so that the students get familiar with the fundamental concepts of different service models
- [end2end](./cloud_intro/end2end/): an end2end excercise to practice in class the use of a full architecture with different components that simulate what they can find in the cloud


**[gcp_setup](./gcp_setup/)**
- [README.md](./gcp_setup/README.md): Instructions to create a GCP account and create a Compute Engine instance
- [excercise_1](./gcp_setup/excercise_1/): Excercise to deploy part of the end2end architecture in GCP

**[gcp_sql](./gcp_sql/)**
- [excercise_postgresql](./gcp_sql/excercise_postgresql/): Excercise to deploy a PostgreSQL instance in GCP, create tables and insert data using Mockaroo
- [excercise_alloy_db](./gcp_sql/excercise_alloy_db/): Excercise to deploy an AlloyDB instance in GCP, and compare it with the performance of PostgreSQL by running some queries
- [excercise_e2e](./gcp_sql/excercise_e2e/): Excercise to deploy an end2end architecture in GCP, using Cloud SQL, PubSub and Compute Engine instances

**[gcp_datawarehouse](./gcp_datawarehouse/)**
- [excercise_bigquery](./gcp_datawarehouse/excercise_bigquery/): Excercise to try the basic functionalities of BigQuery
- [excercise_end2end](./gcp_datawarehouse/excercise_end2end/): Excercise to deploy an end2end architecture in GCP, using Cloud SQL, PubSub, Compute Engine instances and BigQuery

**[gcp_datalake](./gcp_datalake/)**
- [excercise_gcs](./gcp_datalake/excercise_gcs/): Excercise to create a bucket and check its functionality as a object storage container used as a data_lake
- [excercise_end2end](./gcp_datalake/excercise_end2end): Excercise to deploy an end2end architecture in GCP, using Cloud SQL, PubSub, Compute Engine instances, BigQuery and GCS

**[gcp_nosql](./gcp_nosql/)**
- [excercise_stocks](./gcp_nosql/excercise_stocks/): Excercise to use BigTable to store and query stock data
- [excercise_iot](./gcp_nosql/excercise_iot/): Excercise to use an IoT application with Raspberry Pi and BigTable to query temperature data in real time.

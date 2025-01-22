# IoT Excercise

## Overview

This excercise is to demonstrate the use of Google Cloud BigTable to store IoT data.

There are 3 folders in this excercise:

1. `raspberry_pico`: This folder contains the code to run on the Raspberry Pi Pico to simulate the IoT device. It reads the temperature from its internal sensor and it turns on and of the LED.
2. `raspberry_receiver_publisher`: This folder contains the code to run on the Raspberry Pi or local machine to receive the data from the Raspberry Pi Pico and publish it to the Google Cloud Pub/Sub.
3. `big_table_publisher`: This folder contains the code to run locally to receive the data from the Google Cloud Pub/Sub and store it in the Google Cloud BigTable.


## Steps to run

You only have to focus on the `big_table_publisher` folder. The other folders are already configured to work with the Google Cloud Pub/Sub and Google Cloud BigTable.

1. Create a Google Cloud BigTable instance in the GCP console.
2. Write `edem-iot` as the name for the instance and a id.
3. Select SSD storage type.
4. Select europe-west1 as the location.
5. Click on Create.
6. Create a table called `sensors_data`.
7. Create a column family called `measures`.
8. Create a column family called `identification`.

Run the following command to install the dependencies:

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

If your are using Windows, you can activate the virtual environment with the following command:

```bash
.venv\Scripts\activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Change the variables between <> in the `main.py` file with your own values.

Run the following command to start the script:

```bash
GOOGLE_APPLICATION_CREDENTIALS_PUBSUB=<path_to_the_credentials_of_pubsub> GOOGLE_APPLICATION_CREDENTIALS_BIGTABLE=<path_to_your_big_table_credentials> python main.py
```

If you are running from powershell, you can use the following command:

```bash
$env:GOOGLE_APPLICATION_CREDENTIALS_PUBSUB="<path_to_the_credentials_of_pubsub>"; $env:GOOGLE_APPLICATION_CREDENTIALS_BIGTABLE="<path_to_your_big_table_credentials>";
python main.py
```

If you are running from cmd, you can use the following command:

```bash
set GOOGLE_APPLICATION_CREDENTIALS_PUBSUB=<path_to_the_credentials_of_pubsub>
set GOOGLE_APPLICATION_CREDENTIALS_BIGTABLE=<path_to_your_big_table_credentials>
python main.py
```



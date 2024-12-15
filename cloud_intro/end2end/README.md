# END2END Cloud Introduction Excercise

This end2end is inspired in a simplified architecture that you can find in an ecommerce platform

## Architecture

The following image shows the architecture that is used:
![virtual_box_header](.images/architecture_e2e.png)


## Orders App

### To run orders_app

Launch the docker-compose
```sh
docker-compose up -d
```
Run the following command inside orders_app in a VM
```sh
HOST_IP=localhost KAFKA_IP=<delivery-app-host> python -m orders_to_db.main
```

## Delivery App

### To run delivery_app

Launch the docker-compose in Mac
```sh
 HOST_IP=$(ipconfig getifaddr en0) docker-compose up -d
```

Launch the docker-compose in Ubuntu server
```sh
 HOST_IP=$(ip -o -4 addr show wlan0 | awk '{print $4}' | cut -d/ -f1) docker-compose up -d
 ```

Run the following command inside delivery_app in a VM
```sh
KAFKA_IP=<delivery-app-host> python -m delivery_events.main 
```

## Analytical Layer

Launch the docker-compose
```sh
docker-compose up -d
```

Wait for a few minutes until the Metabase container is up and running

To login in the analytical db
```sh
docker exec -it olap_db clickhouse-client
```

To show existing tables after inside the container

```sh
SHOW TABLES FROM analytics_db
````

### To use the analytical_layer
To dowload the clickhouse plugin for metabase

```sh
curl -L -o ./analytical_layer/plugins/clickhouse.metabase-driver.jar https://github.com/ClickHouse/metabase-clickhouse-driver/releases/download/0.9.0/clickhouse.metabase-driver.jar
```

Launch the docker-compose
```sh
docker-compose up -d
```

Run the following command to syncronize the orders table manually within the analytical_layer directory
```sh
HOST_IP=localhost python -m el_orders.main
```

Run the following command to syncronize the delivery table manually within the analytical_layer directory
```sh
HOST_IP=localhost python -m el_delivery.main
```





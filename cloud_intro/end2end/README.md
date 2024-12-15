# END2END Cloud Introduction Excercise

This end2end is inspired in a simplified architecture that you can find in an ecommerce platform

## Architecture

The following image shows the architecture that is used:
![virtual_box_header](.images/architecture_e2e.png)


## Orders App

### To run orders_app

Run the following command inside orders_app in a VM
```sh
HOST_IP=localhost KAFKA_IP=<delivery-app-host> python -m orders_to_db.main
```

## Delivery App

### To run delivery_app

Run the following command inside delivery_app in a VM
```sh
KAFKA_IP=<delivery-app-host> python -m delivery_events_to_db.main 
```

## Analytical Layer

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


#!/bin/bash

export PATH=/usr/local/bin:/usr/bin:/bin
export PYTHONPATH=/app

echo "KAFKA_IP=$KAFKA_IP"
echo "POSTGRES_IP=$POSTGRES_IP"

PYTHON_BIN="/usr/local/bin/python"

echo "[$(date)] Running el_delivery.main..."
$PYTHON_BIN -m el_delivery.main

echo "[$(date)] Running el_orders.main..."
$PYTHON_BIN -m el_orders.main

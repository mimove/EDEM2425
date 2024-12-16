#!/bin/bash

export HOST_IP=${HOST_IP:-localhost}
export KAFKA_IP=${KAFKA_IP:-localhost}  # Default to localhost if not provided

echo "[$(date)] Running el_delivery.main..."
python -m el_delivery.main

echo "[$(date)] Running el_orders.main..."
python -m el_orders.main

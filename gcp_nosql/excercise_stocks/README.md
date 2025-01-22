# GCP BIGTABLE EXERCISE

## Introduction

In this excercise, we will create a simple model in BigTable to simulate a few stocks and their prices. We will use the `google-cloud-bigtable` library to interact with the BigTable instance.


## Setup

1. Create a BigTable instance in the GCP console.
2. Write `edem-stocks` as the name for the instance and a id.
3. Select SSD storage type.
4. Select europe-west1 as the location.
5. Click on Create.


## Create the table

We will use the `cloud shell` to interact with the BigTable instance. Click on the `Activate Cloud Shell` button in the top right corner of the GCP console.


Run the following command to create the tables:

```bash
cbt -instance edem-stocks createtable stocks
cbt -instance edem-stocks createtable stock_prices
cbt -instance edem-stocks createtable market
```


## Create Multiple Column Families

Run the following command to create the column families:

```bash
cbt -instance edem-stocks createfamily stocks details
cbt -instance edem-stocks createfamily stocks financials

cbt -instance edem-stocks createfamily stock_prices price_data
cbt -instance edem-stocks createfamily stock_prices market_conditions

cbt -instance edem-stocks createfamily market info
cbt -instance edem-stocks createfamily market statistics
```


## Insert sample Markets

We will introduce two markets: `NASDAQ` and `Euronext`.

Run the following command to insert the markets:

```bash
# USA Market: NASDAQ
cbt -instance edem-stocks set market market_NASDAQ info:name="NASDAQ"
cbt -instance edem-stocks set market market_NASDAQ info:region="United States"
cbt -instance edem-stocks set market market_NASDAQ info:currency="USD"
cbt -instance edem-stocks set market market_NASDAQ info:trading_hours="09:30-16:00"

cbt -instance edem-stocks set market market_NASDAQ statistics:listed_companies="3300"
cbt -instance edem-stocks set market market_NASDAQ statistics:market_cap="22 Trillion"

# Europe Market: Euronext
cbt -instance edem-stocks set market market_Euronext info:name="Euronext"
cbt -instance edem-stocks set market market_Euronext info:region="Europe"
cbt -instance edem-stocks set market market_Euronext info:currency="EUR"
cbt -instance edem-stocks set market market_Euronext info:trading_hours="08:00-16:30"

cbt -instance edem-stocks set market market_Euronext statistics:listed_companies="1500"
cbt -instance edem-stocks set market market_Euronext statistics:market_cap="7 Trillion"
```

## Insert sample Stocks

We will introduce 2 sample stocks per market.

Run the following command to insert the stocks:

```bash
# NASDAQ (USA) Stocks
cbt -instance edem-stocks set stocks stock_AAPL details:name="Apple Inc."
cbt -instance edem-stocks set stocks stock_AAPL details:sector="Technology"
cbt -instance edem-stocks set stocks stock_AAPL details:exchange="NASDAQ"

cbt -instance edem-stocks set stocks stock_TSLA details:name="Tesla Inc."
cbt -instance edem-stocks set stocks stock_TSLA details:sector="Automotive"
cbt -instance edem-stocks set stocks stock_TSLA details:exchange="NASDAQ"

# Euronext (Europe) Stocks
cbt -instance edem-stocks set stocks stock_ASML details:name="ASML Holding"
cbt -instance edem-stocks set stocks stock_ASML details:sector="Semiconductors"
cbt -instance edem-stocks set stocks stock_ASML details:exchange="Euronext"

cbt -instance edem-stocks set stocks stock_SAN details:name="Santander Bank"
cbt -instance edem-stocks set stocks stock_SAN details:sector="Banking"
cbt -instance edem-stocks set stocks stock_SAN details:exchange="Euronext"
```


## Insert sample Stock Prices

We will introduce the prices for the stocks.

To do that, we will create a simple script in bash to insert the prices for the stocks.

1. Run ```vi stock_prices.sh```
2. Copy the following script:

```bash
# Define markets and stocks
markets=("market_NASDAQ" "market_Euronext")
nasdaq_stocks=("stock_AAPL" "stock_TSLA")
euronext_stocks=("stock_ASML" "stock_SAN")
N=5  # Number of prices per stock per day

# Loop through each market
for market in "${markets[@]}"; do
  if [ "$market" == "market_NASDAQ" ]; then
    stocks=("${nasdaq_stocks[@]}")
  else
    stocks=("${euronext_stocks[@]}")
  fi

  # Loop through each stock in the market
  for stock in "${stocks[@]}"; do
    for day in {1..10}; do
      for price_index in $(seq 1 $N); do
        timestamp="T$((price_index))"

        cbt -instance edem-stocks set stock_prices "$market#$stock#2025-01-$day#$timestamp" \
          price_data:open="$((100 + RANDOM % 50))"

        cbt -instance edem-stocks set stock_prices "$market#$stock#2025-01-$day#$timestamp" \
          price_data:close="$((100 + RANDOM % 50))"

        cbt -instance edem-stocks set stock_prices "$market#$stock#2025-01-$day#$timestamp" \
          price_data:volume="$((500000 + RANDOM % 200000))"

        cbt -instance edem-stocks set stock_prices "$market#$stock#2025-01-$day#$timestamp" \
          market_conditions:sentiment="Positive"

        cbt -instance edem-stocks set stock_prices "$market#$stock#2025-01-$day#$timestamp" \
          market_conditions:volatility="$((10 + RANDOM % 5))"
      done
    done
  done
done
```

3. Run ```chmod +x stock_prices.sh```
4. Run the following command to insert the prices for the stocks:

```bash
nohub ./stock_prices.sh > stock_prices.log 2>&1 &
```

5. To stop the script, run the following command:

```bash
pkill -f stock_prices.sh
```


## Query the data

We can go to Bigtable Studio in the GCP console to query the data. This studio (which is in preview) allows us to interact with the BigTable instance using SQL-like queries.


## Clean up

To delete the BigTable instance, run the following command:

```bash
gcloud bigtable instances delete edem-stocks
```







-- Create the customers table
CREATE TABLE IF NOT EXISTS customers (
    id UInt32,
    name String,
    email String
) ENGINE = MergeTree()
ORDER BY id;

-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    id UInt32,
    name String,
    price Float32
) ENGINE = MergeTree()
ORDER BY id;

-- Create the orders table
CREATE TABLE IF NOT EXISTS orders (
    id UInt32,
    customer_id UInt32,
    timestamp DateTime,
    total_price Float32
) ENGINE = MergeTree()
ORDER BY id;

-- Create the order_products table
CREATE TABLE IF NOT EXISTS order_products (
    order_id UInt32,
    product_id UInt32,
    quantity UInt32,
    price Float32
) ENGINE = MergeTree()
ORDER BY (order_id, product_id);

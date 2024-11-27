import psycopg2

# Connection details
POSTGRES_HOST = "<DB_IP_ADDRESS>"
POSTGRES_PORT = "5432"
POSTGRES_USER = "<edem-username>"
POSTGRES_PASSWORD = "<your-password>"
POSTGRES_DB = "<edem-username>_db"

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    print("Connected to the database!")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE cloud_providers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            year_created INTEGER
        );
    """)
    print("Table 'cloud_providers' created successfully.")

    cursor.execute("""
        INSERT INTO cloud_providers (name, year_created)
        VALUES ('AWS', 2002), ('GCP', 2008), ('AZURE', 2010);
    """)
    connection.commit()
    print("Data inserted successfully.")

    cursor.execute("SELECT * FROM students;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"An error occurred: {e}")

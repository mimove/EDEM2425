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
        CREATE TABLE students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        );
    """)
    print("Table 'students' created successfully.")

    cursor.execute("""
        INSERT INTO students (name, email)
        VALUES ('Alice', 'alice@example.com'), ('Bob', 'bob@example.com');
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

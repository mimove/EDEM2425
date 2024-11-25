from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Default PostgreSQL connection parameters
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "admin"

user_created_db = None


def connect_postgres(dbname="defaultdb"):
    """Connect to a specified PostgreSQL database"""
    return psycopg2.connect(
        dbname=dbname,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )


@app.route('/create_database', methods=['POST'])
def create_database():
    global user_created_db
    try:
        data = request.get_json()
        dbname = data["dbname"]

        # Connect to PostgreSQL to create the new database
        connection = connect_postgres()
        connection.autocommit = True

        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {dbname};")
        cursor.close()
        connection.close()

        user_created_db = dbname

        return jsonify({"message": f"Database '{dbname}' created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/create_user', methods=['POST'])
def create_user():
    global user_created_db
    try:
        if not user_created_db:
            return jsonify({"error": "No database has been created yet."}), 400

        data = request.get_json()
        username = data["username"]
        password = data["password"]

        # Connect to PostgreSQL as the admin user to create the user
        connection = connect_postgres()
        connection.autocommit = True
        cursor = connection.cursor()

        # Create the user
        cursor.execute(f"CREATE USER {username} WITH PASSWORD '{password}';")

        # Grant CONNECT privilege on the user created database
        cursor.execute(f"GRANT CONNECT ON DATABASE {user_created_db} TO {username};")
        cursor.close()
        connection.close()

        # Connect directly to the created database to grant schema privileges
        db_connection = connect_postgres(dbname=user_created_db)
        db_connection.autocommit = True
        db_cursor = db_connection.cursor()

        # Grant privileges on the public schema
        db_cursor.execute(f"GRANT USAGE ON SCHEMA public TO {username};")
        db_cursor.execute(f"GRANT CREATE ON SCHEMA public TO {username};")

        # Set default privileges for any tables created in the future
        db_cursor.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {username};")
        db_cursor.close()
        db_connection.close()

        return jsonify({"message": f"User '{username}' created successfully with privileges on database '{user_created_db}'."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

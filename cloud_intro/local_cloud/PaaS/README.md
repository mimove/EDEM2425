# Run and modify a simple PaaS

For learning the concept of PaaS, two excercises are given. In both cases, you need to use the VM that we have created in the IaaS part, but we will interact differently with it now.

In this case, a pre-made service will be created for you, so you only need to modify a few things and the infrastructure will do the rest for you. In this way, you only have to focus on the code, and not the installation and maintainance of libraries and packages (as in a real PaaS product)

## Excercise

In this excercise, one student sets up a PostgreSQL server with a Flask API to manage database and user creation (as if it was a PaaS provided by a Cloud Provider). The other student interacts with this API to manage databases and connect to them programmatically.

The code is provided in two different folders

- **Student 1** has to open the code inside [excercise_sql_owner](./excercise_sql_owner/)
  - Inside this folder there are two services he has to deploy:
    - A Dockerfile with a postgres image
    - An app.py file with a Flask API for interacting with the Postgres deployed in the container
    - Also the code has to be copied to the VM created at the begginning of the session, this can be done with the scp command:
      ```sh
      scp -r excercise_sql_owner <edem-user>@<edem-user>-vm:~/
      ```
     - Then log-in into the vm
        ```sh
        ssh <edem-user>@<edem-vm>
        cd excercise_sql_owner
        ```

- **Student 2** has to open the code inside [excercise_sql_user](./excercise_sql_user/)
  - Inside this folder there are two scripts that will be used
    - `db_and_user_creation.py` which is used to interact with the API to create a database and a user with a password
    - `sql_interaction.py` with the basic code to create a table, insert a row and make a simple query to the table


### excercise_sql_owner

To deploy both the postgres container, and the API, these steps have to be followed

1. Create a python venv to install the require libraries locally for this excercise without affecting your global python
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. Install the requirements.txt in the newly created .venv
   ```sh
   pip install -r requirements.txt
   ```

3. Build the docker image with that contains the Postgres server
   ```sh
   docker build -t postgres-server .
   ```

4. Deploy the container with the postgres image
   ```sh
   docker run -d --name postgres-server-container -p 5432:5432 postgres-server
   ```

5. Once the container is running, the Flask API can be deployed
   ```sh
   python app.py
   ````

6. If everything has gone as expected, you should see something similar to the following logs:
   ```sh
    * Serving Flask app 'app'
    * Debug mode: off
   WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5000
    * Running on http://192.168.1.144:5000
   Press CTRL+C to quit
   ```

### excercise_sql_user

To interact with the database server that your classmate has created you should follow the next steps:

1. First you need to modify the db_and_user_creation.py script to choose your username, password and db_name

2. After you have modified the file, you can run the script using:
   ```sh
   DB_IP_ADDRESS=<ip-address-vm-student-1> python db_and_user_creation.py
   ```

3. If everything goes as expected, you should see the following logs
   ```sh
    Create Database Response: {'message': "Database '<edem-username>_db}' created successfully."}
    Create User Response: {'message': "User '<edem-username>' created successfully with privileges on database '<edem-username>_db'"}
   ```

4. Now your classmate should also have seen two logs appearing in their screen similar to these ones
   ```ssh
   192.168.1.112 - - [<TIMESTAMP>] "POST /create_database HTTP/1.1" 201 -
   192.168.1.112 - - [<TIMESTAMP>] "POST /create_user HTTP/1.1" 201 -
    ```
    These means that both the `create_database` and `create_user` endpoints have been sucessully called (201 response) using a POST method

5. Now that we have a database and a user, we can use them to create a table and insert a few values on it. To do so, you have to modify the sql_interaction.py script accordingly to what you've done with the previous script. Once you have all set-up, you can run
   ```sh
   python sql_interaction.py
   ```

6. If everything goes as expected, you should see the following logs
   ```sh
   Connected to the database!
   Table 'cloud_providers' created successfully.
   Data inserted successsfully.
   (1, 'AWS', 2002)
   (2, 'GCP', 2008)
   (3, 'AZURE', 2010)
   Connection closed.
   ```






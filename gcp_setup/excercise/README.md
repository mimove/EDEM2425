# Excercise with GCP Resources

We will work on the first components of the architecture we used in the end2end of the module `Cloud Intro`

In particular, we will focus on deploying the `orders-app` and the `delivery-app` in the Cloud, but we will use

## Configure Kafka Cluster

1. Type in the search bar Kafka and open `Managed Service for Apache Kafka`. Enable the API if requested to do so.

2. Once inside the Kafka service, click on `Create`
   ![alt text](.images/kafka-1.png)

3. Give it a name like `edem-kafka-<edem-user>`
4. Select `europe-west1` as the region
5. Click on Grant to allow Kafka configure subnetworks
   ![alt text](.images/kafka-2.png)

6. Select the default network and subnet
7. Leave the rest of the options with their default value, and click on `Create`



### Create the instance for the `orders-app`

For the `orders-app` we will create the VM instance using Google's UI as we did at the beginning of the class.

The characteristics of this instance have to be:

1. Name: orders-app-<edem-user>
2. Region: europe-west1 (Belgium)
3. Image: Debian GNU/Linux 11 (bullseye) on x86/64
4. Machine type: e2-medium (2 vCPU, 1 core, 4 GB memory)
5. Disk size: 10 GB
6. Network: Allow HTTP traffic and HTTPS traffic
7. Network tag: `ejercicio-gcp-setup`

Once the VM instance is created, copy the gcloud command to log into it using a terminal in your laptop.

After you have successfully logged in, follow this steps to install docker:

1. Update de package index:
   ```sh
   sudo apt-get update
   ```

2. Install the necessary packages to allow apt to use a repository over HTTPS:
   ```sh
   sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
   ```

3. Add Docker’s official GPG key:
   ```sh
   curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ````

4. Add Docker's stable repository:
   ```sh
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. Update the package index again:
   ```sh
   sudo apt-get update
   ```

6. Install Docker:
   ```sh
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

7. Add your user to the docker group:
   ```sh
   sudo usermod -aG docker $USER
   ```

8. Log out and log back in so that your group membership is re-evaluated.

9. Verify that Docker is installed correctly by running the hello-world image:
   ```sh
   docker run hello-world
   ```

10. Install docker-compose by downloading the binary:
   ```sh
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   ```

11. Apply executable permissions to the binary:
   ```sh
   sudo chmod +x /usr/local/bin/docker-compose
   ```

12. Verify that docker-compose is installed correctly:
   ```sh
   docker-compose --version
   ```


Now that we have docker and docker-compose installed, we can clone the repository with the `orders-app` code and run it.

1. Clone the repository:
   ```sh
   git clone https://github.com/mimove/EDEM2425.git
   ```

2. Change to the directory of the `orders-app`:
   ```sh
   cd EDEM2425/gcp_setup/excercise/orders-app
   ```


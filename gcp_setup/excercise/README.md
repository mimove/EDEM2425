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

After you have successfully logged in, follow this steps to install docker


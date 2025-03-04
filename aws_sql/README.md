# Configuration of RDS SQL Server on AWS

In this module, we will learn how to configure RDS SQL Server on AWS. First, we will create a new RDS SQL Server instance.

1. Go to the AWS Management Console and open the RDS console.
2. Click on the "Create database" button.
3. Select the "PostgreSQL" engine.
4. Choose the "Free Tier" use case under the Templates section.
5. In Master password, enter `edem2425`
6. Confirm the password.
7. In connectivity, select `Don't connect to an EC2 compute resource`
8. Select yes in the Public access section.
9. In the VPC section, select `Choose existing`
10. Select the VPC you created in the previous module.
11. In Database Authentication, select Password authentication
12. Leave the rest of the settings as default.
13. Click on the "Create database" button.

After the database is created, you can connect to it using a tool like DBeaver. The port number is `5432` and the HOST is the endpoint of the RDS instance. You will have to allow inbound traffic to the port `5432` in the security group of the RDS instance.


# Creation of an AWS Redshift Cluster

Now, we will learn how to create an AWS Redshift cluster.

1. Go to the AWS Management Console and open the Redshift console.
2. Click on the "Create cluster" button.
3. In the Workgroup name, enter `edem-redshift`.
4. In the Database configurations select `admin` for user name
5. Select Manually add the admin password and choose `Edem2425`
6. Go to the IAM and in the User you created for the CLI, add the policy `AmazonRedshiftFullAccess`
7. Click on the "Create cluster" button.

Once the cluster is created, you have to Allow Public Access to the cluster. Go to the cluster details and click on the "Modify" button.

1. In the Publicly accessible section, select `Yes`.
2. Click on the "Modify cluster" button.

After public access is enabled, you have to go to the config of the security group of the cluster and allow inbound traffic to the port `5439`.

Now you can connect to the cluster from the example python code in the `redshift_etl.py` file.


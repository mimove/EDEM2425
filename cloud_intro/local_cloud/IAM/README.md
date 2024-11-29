# Create users and modify permissions

This excercise will show you how to create users and give/remove permissions, similar to what you will have to do in a cloud provider.

This is one of the most important parts of the cloud, and you should always apply the principle of least priviledge, which means that any user should have the minimum permissons that allow him to perform the tasks that they are entitled in any cloud project.

For example, let say we have 3 users in the cloud project of our company:

- A **DevOps/SRE** that handles all the infrastructure of the code
- A **Data Engineer** that is in charge of all the ETLs and maintainance/development of the analytical layer
- A **Business Analyst** that needs to access data to create reports and analyze the different KPIs of the company.


In this scenario, the DevOps/SRE should have a rol of admin, so he is in control of the deployment/maintainance of all the different components of the infrastructure of the company. The DevOps/SRE is also the responsible of the IAM, so they will grant permissions to different users.

The Data Engineer will usually have a rol of user for the infrastucture components, and a role of Admin for all (or some) of the DB Servers deployed/used in the project. By doing this, they can deploy different services to create ETLs and, at the same time, they are allowed to control the creation/modification of data in any/some of the Data Bases.

Finally, the Business Analyst will have a role of reader of the Data, as this person only requires the access to the final layer of pre-proccess data to perform their analysis in a BI tool.


## Excercise

In this excercise you will be in pairs as in the previous one, and we will use the created VM to create a `developer_user` and a `reader_user`. The steps depends on the role you choose (admin or user):


### Admin

You are responsible to create the users and grant them permissions. To do so you have to:

1. Run the following command to create both the developer_user and reader_user with their own home folders:
   ```sh
   sudo useradd -m -s /bin/bash developer_user
   sudo useradd -m -s /bin/bash read_only_user
   ```

2. Now you have to set a default password for each user:
   First for the developer user
   ```sh
   sudo passwd developer_user
   ```

   Then for the reader_user
   ```sh
   sudo passwd read_only_user
   ```
    
3. Create a folder in which both users will have access
   ```sh
   sudo mkdir -p /project/
   ```

4. Set the permissions on that folder, so that the developer can read/write files in that directory
   ```sh
   sudo chown developer_user:developer_user /project/
   sudo chmod 755 /project/
   ```

5. Since you have only given ownership of the folder to the developer user, the read_only_user won't be able to write anything inside that directory


### User

Once your classmate has created the two new roles, now you would be able to have control of the /project/ folder as a developer to run a simple ETL, and then you can test the read_only_user to download the data available in that folder to perform your analysis.




# Create a simple web with nginx

## Steps to follow

The next steps will allow you to create a simple website in your local machine that you can access from your host machine


1. Install nginx with the following command `sudo apt install nginx -y`
2. Once installed, start the nginx service and allow it to be started on startup 
    ```sh
    sudo systemctl start nginx
    sudo systemctl enable nginx
    ```
3. Check the status by running `sudo systemctl status nginx`


Now that the server is created, we will create a simple website

1. Go to the folder html by running `cd /var/www/html`
2. Run `sudo vim index.html`
3. Copy the following code inside (you can modify the text a little bit if you want)
   ```html
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to Nginx!</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is a basic webpage served by Nginx on your VM</p>
    </body>
    </html>
    ````
4. Save by typing `:wq!`
5. Now with the ip address of your machine, you can open a browser and paste the ip address there, you should see a page like the following
![alt text](.images/image.png)



## Additional Excercise

If you want to have a fancier webiste, we can play by adding a css style template and a button using javascript. 

To do so follow the next steps:

1. Replace the content of the index.html file with the following
   ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to My Web Server</title>
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <header>
            <h1>Welcome to My Virtual Machine Web Server</h1>
        </header>
        <section>
            <h2>About This Server</h2>
            <p>This web page is served using Apache/Nginx on an Ubuntu Server Virtual Machine.</p>
            <p>It demonstrates basic web server configuration and hosting capabilities.</p>
        </section>
        <footer>
            <p>&copy; 2024 My Web Server</p>
        </footer>
    </body>
    </html>
    ```

2. Create a folder called `css` by running `sudo mkdir /var/www/html/css`
3. Copy the following content inside the newly created `/var/www/html/css` in a file called `style.css`
   ```css
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f9;
        color: #333;
    }
    header {
        background: #4CAF50;
        color: white;
        padding: 1rem 0;
        text-align: center;
    }
    section {
        margin: 2rem;
        padding: 1rem;
        background: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    footer {
        text-align: center;
        padding: 1rem;
        background: #222;
        color: white;
        margin-top: 2rem;
    }
    ```
    This will change the style of each of the 3 sections of our website

4. Create a folder called `js` by running `sudo mkdir /var/www/html/js`
5. Copy the following content inside the newly created folder in file called `script.js`
   ```js
    document.addEventListener("DOMContentLoaded", () => {
        const button = document.createElement("button");
        button.textContent = "Click Me!";
        button.style.padding = "10px 20px";
        button.style.fontSize = "16px";
        button.addEventListener("click", () => {
            alert("Hello, World!");
        });
        document.body.appendChild(button);
    });
    ```
6. With this little js example, we can now add a button to our website. Modify your html section, and add a line before `</section>` with this content: `<script src="js/script.js"></script>`
   
7. Refresh the browser where you have copied the ip address of the vm. You should see something like this
   ![alt text](.images/image-1.png)

8. Try pressing the button!!






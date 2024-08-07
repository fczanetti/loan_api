# Manual deploy to Digital Ocean

This step by step will allow you to deploy a simple application to a Digital Ocean Droplet. We are using an application that I called Loan API, and it is just a simple API to manage loans and payments.

The goal here is not to implement all the resources necessary for an application to run safely on a remote server, but it can be nice for testing or even for learning some new commands.

We are using docker compose to 
manage our containers in production environment and, as it is a simple application just for learning purposes, our Nginx, 
PostgreSQL database and application will all run inside the same Droplet.

Some paid resources from Digital Ocean will be necessary, but the cost will not be high since the purpose here is just 
learn how to deploy. When finished, we can delete everything from the platform.

## Create an account on Digital Ocean

First we have to create an account on Digital Ocean. [This link](https://cloud.digitalocean.com/registrations/new) might help.

## Create a new Droplet and add an SSH key to it

Once we have an account, we can create a new Droplet. Make sure you choose the most basic options, it will be enough for
running this application. Remember to choose an Ubuntu image for it and also SSH as the authentication method.

## Clone the repository

If you woud like to see the repository before clonning you can [use this link](https://github.com/fczanetti/loan_api).

Besides clonning we have to be able to run the Django 'collectstatic' command. This will create a 'staticfiles' directory that we are going to use later.  

```
git clone git@github.com:fczanetti/loan_api.git

# These next 4 commands are necessary for us to have our staticfiles directory created
pipenv sync -d
pipenv shell
cp contrib/env-sample .env
python manage.py collectstatic
```

## Send the 'non root user' script to the droplet

For safety reasons, it is advised to only connect to your Droplet with the root user when necessary. This put, it's nice to have another user to connect through. Inside the 'deploy_do' directory there is a script named 'non_root_user.sh'. Use the following command to send a copy of this file to our 'home' directory inside our Droplet. The Droplet IP address will be necessary, but it can be easily found in the droplets page.

```
scp deploy_do/non_root_user.sh root@<DROPLET_IP_ADDRESS>:/home/
```

## Access the Droplet

Now we can access the Droplet. This first time we have to use the root user, but later it won't be necessary anymore.
```
ssh root@<DROPLET_IP_ADDRESS>
```

## Execute the script sent to create a new 'non root' user

Inside the Droplet, we can use this command to run the non_root_user.sh script and create a new user. Some basic questions
will be asked, and the most important is the 'username' chosen, because we'll use it to reconnect later.
```
/home/non_root_user.sh
```
After creating the new user we can run the command ```exit``` to leave the Droplet.

## Access the Droplet using the new user to make sure it worked

Now that we have a new user we can use it to access our Droplet. The NEW_USER is the username chosen when 
creating the 'non root user'.
```
ssh <NEW_USER>@<DROPLET_IP_ADDRESS>
```

## Install Docker on the new Droplet

Docker will be necessary for us to run the application inside the Droplet, and Digital Ocean has [this nice tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) that can help us with this task.

## Create an image of the application

Now we have to create an image for the application that we want to deploy. In the **root directory** of the app, use the command bellow for it. You can choose a name for the image, the VERSION can be 1.0.0, and the dot (.) in the ent of the command indicates the path to the Dockerfile, in this case the same directory from where we are running the command.
```
docker build -t IMAGE_NAME:VERSION .
```

## Save the image as a tag.gz file

The next command can be used to save our image in a tar.gz file. Choose also a name for this file.

```
docker save <IMAGE_NAME:VERSION> | gzip > NAME_OF_FILE.tar.gz
```

## Send the image to the Droplet

Once we have a file, we can use the commands below to send a copy of it to our Droplet.
```
# before sending, run this command from inside the Droplet to create a directory for the files that will be sent
mkdir /home/<NEW_USER>/app 

# once the directory is created you can leave the Droplet and run this one
scp NAME_OF_FILE.tar.gz <NEW_USER>@DROPLET_IP_ADDRESS:/home/<NEW_USER>/app
```

## Send also the other necessary files to the Droplet

For this application, we also have to send some other files so everything works fine. Note that, to send directories, the option '-r' has to be used (staticfiles directory).
``` 
scp start.sh <NEW_USER>@DROPLET_IP_ADDRESS:/home/<NEW_USER>/app
scp deploy_do/docker-compose-prod.yml <NEW_USER>@DROPLET_IP_ADDRESS:/home/<NEW_USER>/app
scp contrib/env-sample <NEW_USER>@DROPLET_IP_ADDRESS:/home/<NEW_USER>/app/.env
scp nginx/nginx.conf <NEW_USER>@DROPLET_IP_ADDRESS:/home/<NEW_USER>/app
scp -r staticfiles <NEW_USER>@DROPLET_IP_ADDRESS:/home/<NEW_USER>/app
```
Now our 'app' folder inside the Droplet should look like this:
```
├── 📂 home
|   ├── 📂 NEW_USER
|   |   ├── 📂 app
|   |   |   ├── start.sh
|   |   |   ├── docker-compose-prod.yml
|   |   |   ├── .env
|   |   |   ├── nginx.conf
|   |   |   ├── NAME_OF_FILE.tar.gz
|   |   |   ├── 📂 staticfiles
```

## Adjust the .env file sent with the correct values

As a suggestion for the SECRET_KEY, Django has a function called get_random_secret_key. This function
can be imported from django.core.management.utils and executed to return a value that can be used. It's 
also nice to have a Sentry integration (SENTRY_DSN), but if you don't want to create it now it can be blank, 
the application should work without it.

Choose a value for POSTGRES_PASSWORD, POSTGRES_USER and POSTGRES_DB. After filling the individual values, use
them in the DATABASE_URL as well.
```
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=<DROPLET_IP_ADDRESS>

DATABASE_URL=postgres://<POSTGRES_USER>:<POSTGRES_PASSWORD>@database:5432/<POSTGRES_DB>
POSTGRES_PASSWORD=
POSTGRES_USER=
POSTGRES_DB=

SENTRY_DSN=
```

## Load the image sent to the Droplet

Use the next command inside the Droplet to load the Docker image from the file sent before.
```
docker load --input /home/<NEW_USER>/app/NAME_OF_FILE.tar.gz
```
You can check if the image was loaded using the command ```docker images```. If it was successfull, 
the image will be listed in the result.

## Start the containers

After the image loaded and everything else set we can start our containers.
```
docker compose -f /home/<NEW_USER>/docker-compose-prod.yml up
```
This command will run a PostgreSQL database, our app and an Nginx server that works as a simple proxy and 
also serves static files. The static files are only used if you access Django REST brownsable API page.

## Access app container and load initial data

To be able to test some requests we can loan some initial data in our database. First, run the
following command to list our running containers:
```
docker ps
```

One of the three containers is called 'loan_api_prod_app'. We need its ID to run the next command:
```
docker exec CONTAINER_ID python manage.py loaddata initial_data.json
```
After running this command you created some instances and saved to the database:
- User:
    - email: admin@admin.com
    - password: admin
- Bank:
    - ID: 1
    - name: First Bank
- Bank:
    - ID: 2
    - name: Second Bank

## Test requests

You can use the load data from the previous step to test some requests. The root endpoint will be ```http://<DROPLET_IP_ADDRESS>/```.

Follow the [project documentation](https://github.com/fczanetti/loan_api?tab=readme-ov-file#authentication) to check how you can create tokens, create loans, payments etc.


## References
The 'non_root_user.sh' script was based on a script that I caught from this blog post:
- https://huogerac.hashnode.dev/how-to-add-wildcard-https-on-digitalocean-using-certbot-ubuntu-20-nginx

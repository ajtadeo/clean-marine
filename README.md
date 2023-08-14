# Clean Marine <!-- omit from toc -->

This web app serves as a centralized hub for information about local beach clean up events, originally created for the [HOTHX hackathon](https://hothx.devpost.com/), hosted by UCLA ACM Hack in 2023. 

Clean Marine was built using the Python Django full-stack webframework for hosting th SQLite database and web server, webscraping scripts using Selenium and Beautiful Soup, and the Google Maps API to provide users a visual guide on locating nearby events. Additionally, this app has been Dockerizied allowing it to be run in any environment (with Docker installed) with a simplified setup process. This feature was implemented for [Paramount Data and Decision Science Group's](https://science.viacom.com/) Hackweek 2023 to research how to Dockerize multi-container applications. 

HothX Presentation and Demo: https://youtu.be/zuwXPLttlSM

### Table of Contents <!-- omit from toc -->
- [Docker Setup](#docker-setup)
  - [Steps](#steps)
  - [Docker-ization Steps](#docker-ization-steps)
  - [Making Changes](#making-changes)
- [Invoke Commands](#invoke-commands)
  - [`invoke scrape`](#invoke-scrape)
  - [`invoke dump`](#invoke-dump)
- [Database Manipulation](#database-manipulation)
  - [View Table Structure](#view-table-structure)
  - [Update Table Structure](#update-table-structure)
  - [Delete the Table](#delete-the-table)
  - [Create the Table](#create-the-table)
- [Conda Setup (Deprecated)](#conda-setup-deprecated)
  - [Steps](#steps-1)
  - [Updating dependencies](#updating-dependencies)
- [Resources](#resources)

## Docker Setup

### Steps
1. Install Docker Desktop.
2. Execute `docker compose up` in the project root directory.

### Docker-ization Steps 

Originally, Clean Marine was setup using a conda virtual environment. The code for this implementation can be viewed [here](https://github.com/ajtadeo/clean-marine/tree/c26fa3cb93f0fc2f91ffa6ca971f8beea70b6b69). The following steps were taken to Dockerize the application to the current implementation:

1. Convert `base.yml` to `requirements.txt`.
    ```sh
    pip freeze > requirements.txt
    ```
2. Fill out `.env` with the following credentials. If `.env` hasn't already been created, create it.
   ```env
   GOOGLE_MAPS_KEY=secret
   SECRET_KEY=secret
   ```
   NOTE: We can't use [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/) because this app isn't configured as a Docker Swarm. 
3. In the root directory, initialize Docker files and create an image of the application
    ```
    docker init
        ? What application platform does your project use? Python
        ? What version of Python do you want to use? 3.11.4
        ? What port do you want your app to listen on? 8000
        ? What is the command to run your app? python manage.py runserver 0.0.0.0:8000
    ```
    Now, the file structure should look like this:
    ```
    clean-marine/           <-- Django project root     
    ├── clean-marine/       <-- clean-marine app, contains settings and configuration
    ├── dashboard/          <-- dashboard app
    │   ├── static/
    │   ├── templates/
    │   ├── base.yml
    │   ├── db.sqlite3
    │   ├── dump.json
    │   ├── manage.py
    │   ├── notes.txt
    │   └── tasks.py
    ├── components/         <-- components
    │   └── event/
    ├── .gitignore
    ├── .dockerignore       <-- NEW
    ├── .env
    ├── .gitignore
    ├── compose.yaml        <-- NEW
    ├── Dockerfile          <-- NEW
    ├── manage.py
    ├── tasks.py
    ├── requirements.txt
    └── README.md
    ```
4. Update `compose.yaml` to reference `.env` as the environment variables file.
    ```yaml
   services:
     django:
       build:
         context: .
       ports:
         - 8000:8000
       env_file:
         - ./.env
    ```
    NOTE: Selenium must be added as a service to fix the broken webscrapers. This will be implemented in a future update.
5. In `clean-marine/settings.py`, add `0.0.0.0` to `ALLOWED-HOSTS` to let the user connect to the Django app through the isolated Docker environment.
   ```python
   # ...
   ALLOWED_HOSTS = ['0.0.0.0']
   # ...
   ```
6. Create the Docker image and run the service
    ```sh
    docker compose up
    ```
    Visit your newly Docker-ized app at `0.0.0.0:8000` :partying_face:!

    NOTE: The Docker images in this multi-container app have the format `clean-marine-[service]`. 
7. To stop the app, either click `Ctrl-C` in the terminal or run `docker compose down` in a seperate terminal.

### Making Changes
If changes are made to the Django app or the Docker configuration files, its necessary to remove the containers and images and create new ones. 

1. Stop any running containers by either clicking `Ctrl-C` in the terminal or run `docker compose down` in a seperate terminal. These commands will also remove the containers.
2. Verify the containers were removed.
    ```sh
    docker ps -a
    ```
3. Remove the image.
   ```sh
   docker image rm clean-marine-django
   ```
4. Verify the image was removed.
   ```sh
   docker images
   ```
5. Recreate the image.

   ```sh
   docker compose up
   ```

<!-- 7. Verify the image was created
   ```
   docker images
   ```
1. Run the Docker container, adding to Docker Desktop as `cm-django`. `--publish [host port]:[container port]` allows the isolated Docker container to be accessed by the outside world. 
    ```
    docker run --publish 8000:8000 --name cm-django cm-django
    ```
2.  To start, stop, and restart the Docker container:
    ```
    docker start cm-django
    docker stop cm-django
    docker restart cm-django
    ```
    Note: `docker start cm-django` starts the server in the background, so you have to use `docker stop cm-django` instead of Ctrl-C to stop it.
3.  Create a volume which will be used to persist the data generated and used by Docker containers. The volume communicates with the container via a user-defined bridge network. Mounting the volume establishes a connection over this network when using `docker run`.
    ```
    docker volume create cm-sqlite-db
    docker network create sqlite-net
    ``` -->

## Invoke Commands

Invoke commands are this app's custom CLI, used for simplifying tasks that are done regularly. Run these commands from the root directory `clean-marine`.

### `invoke scrape`

* Runs all web scrapers and updates the database with new information.
* Currently implemented web scrapers:
    * Surfrider Foundation

### `invoke dump`

* Dumps data from the SQLite database into `dump.json` in the project root directory.

## Database Manipulation

### View Table Structure
1. In the terminal:
    ```sh
    python3 manage.py dbshell
    ```
2. In the dbshell:
    ```sql
    .header on
    .mode column
    pragma table_info('dashboard_events');
    ```

### Update Table Structure
1. Make changes to `dashboard/models.py`
2. In the terminal in the root directory:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

### Delete the Table
Sometimes it's best to just start from scratch and rerun the webscraper ;-;

1. In the terminal:
    ```sh
    python manage.py dbshell
    ```
2. In the dbshell:
    ```sql
    DROP TABLE dashboard_events;
    ```

### Create the Table
1. In the terminal:
    ```sh
    python manage.py dbshell
    ```
2. In the dbshell:
    ```sql
    CREATE TABLE dashboard_events (
        id INTEGER PRIMARY KEY NOT NULL,
        eventname TEXT NOT NULL UNIQUE,
        organization TEXT NOT NULL,
        link TEXT NOT NULL,
        datetime TEXT,
        location TEXT,
        lng FLOAT,
        lat FLOAT
    );
    ```

## Conda Setup (Deprecated)

### Steps

1. Install python3 and the [Chrome driver](https://chromedriver.storage.googleapis.com/index.html?path=111.0.5563.41/) for web scraping on your machine
1. Clone the repository and cd into it.
    ```sh
    git clone https://github.com/ajtadeo/clean-marine.git
    cd clean-marine
    ```
3. Set up the virtual environment.
    * Create the virutal environment.
        ```sh
        conda env create -f base.yml
        ```
    * Verify that the virtual environment was created correctly.
        ```sh
        conda info --envs
        ```
    * Activate the virtual environment.
        ```sh
        conda activate cm_base
        ```
4. Migrate and update the SQLite database. Currently, running `./manage.py makemigrations` makes migrations and scrapes the web since there is no automated scraping capability. 
    ```sh
    ./manage.py makemigrations
    ./manage.py migrate
    ```
5. Start the development server.
    ```sh
    ./manage.py runserver
    ```

### Updating dependencies

1. Update dependencies under `pip` in `base.yml`.
2. Deactivate the virtual environment if it is currently running.
    ```sh
    conda deactivate
    ```
3. Update the virtual environment. 
    * If you are removing a dependency, removing and recreating the virtual environment is necessary since `--prune` does not work as of August 9 2023. 
        ```sh
        conda remove --name cm_base --all
        conda env create -f base.yml
        ```
    * Otherwise, update the virtual environment as normal.
        ```sh
        conda env update -f base.yml
        ```
4. Verify that the virtual environment was updated correctly.
    ```sh
    conda info --envs
    ```
5. Activate the virtual environment.
    ```sh
    conda activate cm_base
    ```
6. Verify that the new dependency was added to the virtual environment.
    ```sh
    pip list --local
    ```

## Resources

* [Django Components Documentation](https://github.com/EmilStenstrom/django-components)
* [SQLite Creating and Dropping Tables](https://www.sqlitetutorial.net/sqlite-drop-table/)
* [Converting SQLite DB from local to Docker](https://raphaelpralat.medium.com/how-to-run-local-sqlite-commands-in-a-docker-container-bcba18af69f2)
* [Setting Environtment Variables in Docker](https://docs.docker.com/compose/environment-variables/set-environment-variables/)
* [Docker Python documentation](https://docs.docker.com/language/python/)
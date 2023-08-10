# Clean Marine

HothX Presentation and Demo: https://youtu.be/zuwXPLttlSM

## About

Our web app seeks to centralize information about local beach clean up events for those that wish to voluneer. We built Clean Marine using the Django full-stack Webframework to host our SQL database and web server, wrote webscraping scripts using Selenium and Beautiful Soup, and using the Google Maps API to provide users a visual guide on locating nearby events.

In the future, we'd like to integrate more volunteer organizations in our web scraper scripts and create a filtering tool for users to view events from certain organizations or within a certain distance. Additionally, we'd like to display the locations of each event listed on Clean Marine in the Google Maps component.

## Setup

1. Install python3 and the [Chrome driver](https://chromedriver.storage.googleapis.com/index.html?path=111.0.5563.41/) for web scraping on your machine
1. Clone the repository and cd into it.
    ```
    git clone https://github.com/ajtadeo/clean-marine.git
    cd clean-marine
    ```
3. Set up the virtual environment.
    * Create the virutal environment.
        ```
        conda env create -f base.yml
        ```
    * Verify that the virtual environment was created correctly.
        ```
        conda info --envs
        ```
    * Activate the virtual environment.
        ```
        conda activate cm_base
        ```
4. Migrate and update the SQLite database. Currently, running `./manage.py makemigrations` makes migrations and scrapes the web since there is no automated scraping capability. 
    ```
    ./manage.py makemigrations
    ./manage.py migrate
    ```
5. Start the development server.
    ```
    ./manage.py runserver
    ```

## Updating dependencies

1. Update dependencies under `pip` in `base.yml`.
2. Deactivate the virtual environment if it is currently running.
    ```
    conda deactivate
    ```
3. Update the virtual environment. 
    * If you are removing a dependency, removing and recreating the virtual environment is necessary since `--prune` does not work as of August 9 2023. 
        ```
        conda remove --name cm_base --all
        conda env create -f base.yml
        ```
    * Otherwise, update the virtual environment as normal.
        ```
        conda env update -f base.yml
        ```
4. Verify that the virtual environment was updated correctly.
    ```
    conda info --envs
    ```
5. Activate the virtual environment.
    ```
    conda activate cm_base
    ```
6. Verify that the new dependency was added to the virtual environment.
    ```
    pip list --local
    ```

## Invoke Commands

Invoke commands are this app's custom CLI, used for simplifying tasks that are done regularly. Run these commands from the root directory `clean-marine`.

#### `invoke scrape`

* Runs all web scrapers and updates the database with new information.
* Currently implemented web scrapers:
    * Surfrider Foundation
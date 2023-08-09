# Clean Marine

HothX Presentation and Demo: https://youtu.be/zuwXPLttlSM

## About

Our web app seeks to centralize information about local beach clean up events for those that wish to voluneer. We built Clean Marine using the Django full-stack Webframework to host our SQL database and web server, wrote webscraping scripts using Selenium and Beautiful Soup, and using the Google Maps API to provide users a visual guide on locating nearby events.

In the future, we'd like to integrate more volunteer organizations in our web scraper scripts and create a filtering tool for users to view events from certain organizations or within a certain distance. Additionally, we'd like to display the locations of each event listed on Clean Marine in the Google Maps component.

## Setup

1. Install python3 and the Chrome driver for web scraping (https://chromedriver.storage.googleapis.com/index.html?path=111.0.5563.41/) on your machine
1. ```git clone https://github.com/ajtadeo/clean-marine.git```
2. ```cd clean-marine```
3. ```pip3 install pipenv```
4. ```pipenv shell```
5. ```pip3 install django selenium django_components webdriver_manager```

## Updating the SQL Database
1. ```python manage.py makemigrations```
2. ```python manage.py migrate```

## Running the Development Server
1. ```python manage.py runserver``` 
2. Open the web page at http://localhost:8000/


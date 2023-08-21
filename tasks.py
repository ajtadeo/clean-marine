# invoke commands
from invoke import task, run
import os
import django
import requests
from stat import *
# from xml.etree import ElementTree
# from os import listdir
# from os.path import isfile, join

# this setup needs to be at the top in order to execute the webscraper the app's context
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clean-marine.settings")
django.setup()

# web scraping
# from bs4 import BeautifulSoup
# import json
# from datetime import datetime
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dashboard.models import Events

# @task
# def commit(context, name='base'):
#   """
#   Shortcut for committing your changes

#   Args:
#       context: required for all invoke tasks
#       name: name of the developer (defaults to base)

#   To do:
#       - check that coverage is up to date

#   Example:    invoke commit --name=amy

SURFRIDER_URL = 'https://volunteer.surfrider.org'


@task
def scrape(context, env='cm_base'):
    """ Run webscrapers for all websites """
    scrape_surfrider()


def scrape_surfrider():
    """ Run webscraper for Surfrider website """
    try:
        print('Starting Surfrider web scraper...')
        # set up options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        options.add_argument('--blink-settings=imagesEnabled=false')
        # options.add_argument("--disable-dev-shm-usage")

        print(options.arguments)

        # set up driver
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver = webdriver.Chrome(service=Service(executable_path='/usr/bin/chromedriver-linux64/chromedriver'), options=options)
        driver.get(SURFRIDER_URL)

        # wait for page to load, then scrape all available events
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article.opportunityCard"))
        )
        events = driver.find_elements(By.CSS_SELECTOR, "article.opportunityCard")
        print(str(len(events)) + " events found.")
        events_successful = 0
        for event in events:
            events_successful += scrape_surfrider_event(event)
        print(str(events_successful) + " events scraped successfully.")
        driver.quit()
    except Exception as err:
        print('[ERROR] The scraping job failed. See exception:')
        print(err)
    print("Done.")


def scrape_surfrider_event(event):
    """ Helper function for Surfrider web scraping and saving to DB """

    # scrape information from the event card
    try:
        link = event.find_element(By.TAG_NAME, "a").get_attribute("href")
        eventname = event.find_element(By.TAG_NAME, "h2").text
        organization = event.find_element(By.TAG_NAME, "h3").text

        datetime_location = event.find_elements(By.TAG_NAME, "li")
        datetime = datetime_location[0].text
        if (len(datetime_location) == 2):
            location_raw = datetime_location[1].text
            location = location_raw.replace("Location: ", "")
        else:
            location = ""
        
        # if location is blank, then the coordinates request will fail and the object will be {'latitude': None, 'longitude': None}
        lat, lng = get_coordinates(urllib.parse.quote_plus(location))

        result = {
            "eventname": eventname,
            "organization": organization,
            "link": link,
            "datetime": datetime,
            "location": location,
            "lat": lat,
            "lng": lng
        }

        # save to DB
        save(result)
        return 1
    
    except Exception as err:
        print("[ERROR] Scraping Surfrider event card failed.")
        print(err)
        return 0


def get_coordinates(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": os.getenv("GOOGLE_MAPS_KEY")
    }
    res = requests.get(url, params=params)
    data = res.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        return float(latitude), float(longitude)
    else:
        print(F"Geocoding failed for {address}:", data["status"])
        return None, None


def save(event):
    """ Load a JSON format event into the DB """
    try:
        Events.objects.create(
            eventname=event['eventname'],
            organization=event['organization'],
            link=event['link'],
            datetime=event['datetime'],
            location=event['location'],
            lat=event['lat'],
            lng=event['lng'],
        )
    except Exception as e:
        print('[ERROR] Saving to DB failed. See exception:')
        print(e)


@task
def dump(context, env='cm_base'):
    """ Dumps Events table into dump.json """
    cmd = './manage.py dumpdata dashboard.Events --natural-primary > dump.json'
    run(cmd)
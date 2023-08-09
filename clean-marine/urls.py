"""clean-marine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views import home_page_view

# scraping tools
from bs4 import BeautifulSoup
import json
from datetime import datetime
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webscraper.models import Events

urlpatterns = [
    path("", home_page_view, name='home'),
    path('admin/', admin.site.urls),
    # path('command/<int:id>/cmd', command)
]

# ===== Scrape Tool ===== #
SURFRIDER_URL = 'https://volunteer.surfrider.org'
DRIVER_PATH = "/Users/ajtadeo/chromedriver_mac64/chromedriver"


# This function scrapes the Surfrider Foundation website for events
def scrape_surfrider():
    e_list = []
    try:
        print('Starting the scraping tool')
        # set up options
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument("--disable-gpu")
        options.add_argument('--blink-settings=imagesEnabled=false')

        # set up driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(SURFRIDER_URL)

        # get 2 events from the page
        e = driver.find_element(By.CLASS_NAME, 'opportunityCard')
        e_list.append(scrape_event(e))
        e = e.find_element(By.XPATH, "//article/following-sibling::article")
        e_list.append(scrape_event(e))
    except Exception as err:
        print('The scraping job failed. See exception:')
        print(err)
    print(e_list)
    save_function(e_list)


def scrape_event(event):
    link = event.find_element(By.TAG_NAME, "a").get_attribute("href")
    eventname = event.find_element(By.TAG_NAME, "h2").text
    organization = event.find_element(By.TAG_NAME, "h3").text

    dateTime_and_location = event.find_elements(By.TAG_NAME, "li")
    date_and_time = dateTime_and_location[0].find_element(By.CLASS_NAME, "timeDetails").text
    location = dateTime_and_location[1].text

    result = {
        "placeid": "",
        "eventname": eventname,
        "organization": organization,
        "link": link,
        "date_and_time": date_and_time,
        "location": location,
    }
    return result


# This function takes a list of JSON events and loads them into the database
def save_function(event_list):
    new_count = 0

    for event in event_list:
        try:
            Events.objects.create(
                placeid=urllib.parse.quote_plus(event['location']),
                eventname=event['eventname'],
                organization=event['organization'],
                link=event['link'],
                date_and_time=event['date_and_time'],
                location=event['location'],
            )
            new_count += 1
        except Exception as e:
            print('failed at latest_event is none')
            print(e)
            break
    # return print('finished')

# scrape_surfrider()
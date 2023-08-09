from django.shortcuts import render
from django.views import generic
from django.db import models
from webscraper.models import Events

from dotenv import load_dotenv
import os

load_dotenv()

def save_function(event_list):
    new_count = 0

    for event in event_list:
        try:
            Events.objects.create(
                eventname = event['eventname'],
                organization = event['organization'],
                link = event['link'],
                date_and_time = event['date_and_time'],
                location = event['location'],
                placeid = event['placeid']
            )
            new_count += 1
        except Exception as e:
            print('failed at latest_event is none')
            print(e)
            break
    # return print('finished')

# # replace the following line with the webscraper function
# save_function([{
# 'eventname': 'anameofanevent',
# 'organization': 'Surfrider',
# 'link': 'https://volunteer.surfrider.org',
# 'date_and_time': '2021-09-25T09:00:00-07:00',
# 'location': 'San Diego, CA',
# 'placeid': 'ChIJN1t_tDeuEmsRUsoyG83frY4'
# }])


def home_page_view(request):
    context = {}
    context['events'] = Events.objects.all()
    context['key'] = os.getenv("GOOGLE_MAPS_KEY")
    return render(request, 'home.html', context)
from django.shortcuts import render
from django.views import generic
from django.db import models
from django.core import serializers
from dashboard.models import Events

import os


def home_page_view(request):
    # need to serialize the objects so the javascript code works
    events = Events.objects.all()
    serialized_events = serializers.serialize("json", events)

    context = {
        'events_serialized': serialized_events,
        'events': events,
        'key': os.getenv("GOOGLE_MAPS_KEY")
    }
    return render(request, './home.html', context)
# This file contains an explanation for how the SQL database should be structured.
# To update the SQL database after making changes here, type the following commands:
# python manage.py makemigrations
# python manage.py migrate

from django.db import models


# This is the model for the Events table.
# id is the PRIMARY KEY, used to uniquely identify entries in the table
class Events(models.Model):
    eventname = models.CharField(max_length=200, unique=True)
    organization = models.CharField(max_length=200)
    link = models.CharField(max_length=2083)
    datetime = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.eventname
    
    def __repr__(self):
        return "Events()"
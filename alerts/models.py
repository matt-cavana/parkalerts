# models.py
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os

class AlertType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    icon_url = models.CharField(max_length=200) 
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact = models.CharField(max_length=100)
    email = models.EmailField()
    rprkid = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Alert(models.Model):
    title = models.CharField(max_length=200)
    alert_type = models.ForeignKey('AlertType', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    details = models.TextField()
    publish_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    kml_file = models.FileField(upload_to='map_layers/', null=True, blank=True)
    affected_sites = models.TextField(blank=True, null=True)
    website_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
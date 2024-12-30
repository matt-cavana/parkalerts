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
    
class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True, db_column='ContactId')
    office_name = models.CharField(max_length=255, db_column='OfficeName')
    email = models.EmailField(db_column='Email')
    phone = models.CharField(max_length=50, db_column='Phone')
    address = models.TextField(db_column='Address')
    office_hours = models.TextField(db_column='OfficeHours')
    create_date = models.DateTimeField(db_column='CreateDate')
    created_by = models.CharField(max_length=100, db_column='CreatedBy')
    last_update = models.DateTimeField(null=True, blank=True, db_column='LastUpdate')
    updated_by = models.CharField(max_length=100, null=True, blank=True, db_column='UpdatedBy')

    def __str__(self):
        return self.office_name
    
from django.db import models
from django.utils import timezone

class Location(models.Model):
    parkId = models.IntegerField(primary_key=True, db_column='parkid')
    RPrkId = models.IntegerField(db_column='rprkid', default=0)
    name = models.CharField(max_length=100, default='')
    tenure = models.CharField(max_length=100, default='')
    region = models.CharField(max_length=100, default='')
    district = models.CharField(max_length=100, default='')
    longitude = models.FloatField()
    latitude = models.FloatField()
    status = models.CharField(max_length=50, default='')
    create_date = models.DateTimeField(db_column='createdate', default=timezone.now)
    created_by = models.CharField(max_length=100, db_column='createdby', default='unknown')
    contact = models.ForeignKey(
        'Contact',  # Refers to the Contact model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='contactid',
        related_name='locations'
    )

    def __str__(self):
        return self.name
    
class Alert(models.Model):
    title = models.CharField(max_length=200)
    alert_type = models.ForeignKey('AlertType', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, db_column='location_id', to_field='parkId')
    details = models.TextField()
    publish_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    kml_file = models.FileField(upload_to='map_layers/', null=True, blank=True)
    affected_sites = models.TextField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
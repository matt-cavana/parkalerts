# alerts/serializers.py

from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(source='location.latitude')
    longitude = serializers.FloatField(source='location.longitude')

    class Meta:
        model = Alert
        fields = ['title', 'alert_type', 'location', 'details', 'publish_date', 'start_date', 'end_date', 'published', 'latitude', 'longitude']

# alerts/views.py
import os
import json
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.core.serializers import serialize
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.http import HttpResponse
from django.http import JsonResponse
from .serializers import AlertSerializer
from .models import Alert
from .forms import AlertForm
from django.utils.timesince import timesince
from django.utils.timezone import now, localtime
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime
import pytz

class AlertCreateView(CreateView):
    model = Alert
    form_class = AlertForm
    template_name = 'alerts/alert_form.html'
    success_url = reverse_lazy('alert_list')

class AlertUpdateView(UpdateView):
    model = Alert
    form_class = AlertForm
    template_name = 'alerts/alert_form.html'
    success_url = reverse_lazy('alert_list')

class AlertDeleteView(DeleteView):
    model = Alert
    success_url = reverse_lazy('alert_list')
    template_name = 'alerts/alert_confirm_delete.html'

# Calculate time since published
def get_time_elapsed(publish_date):
    now = localtime()
    diff = now - publish_date
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return f"{diff.seconds} second{'s' if diff.seconds > 1 else ''} ago"

# Home page view
def home_page(request):
    alerts = Alert.objects.filter(published=True).select_related('alert_type').order_by('-start_date')
    alerts_data = []
    for alert in alerts:
        alert.time_elapsed = get_time_elapsed(alert.publish_date) if alert.publish_date else 'Not published'
        icon_path = alert.alert_type.icon_url if alert.alert_type and alert.alert_type.icon_url else 'images/default-icon.png'
        icon_url = static(icon_path)

        latitude = alert.location.latitude if alert.location else None
        longitude = alert.location.longitude if alert.location else None
        location_name = alert.location.name if alert.location else 'Unknown Location'

        alerts_data.append({
            'title': alert.title,
            'details': alert.details,
            'affected_sites': alert.affected_sites,
            'website_link': alert.website_link,
            'latitude': latitude,
            'longitude': longitude,
            'location': location_name,
            'alert_type': alert.alert_type.name,
            'start_date': alert.start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': alert.end_date.strftime('%Y-%m-%d %H:%M:%S') if alert.end_date else '',
            'icon_url': icon_url,
            'attachment': alert.attachment.url if alert.attachment else '',
            'attachment_name': os.path.basename(alert.attachment.name) if alert.attachment else '',
            'publish_date': alert.publish_date.strftime('%Y-%m-%d %H:%M:%S') if alert.publish_date else '',
            'time_elapsed': alert.time_elapsed,
            'kml_file_url': alert.kml_file.url if alert.kml_file else '',
        })

    alerts_json = json.dumps(alerts_data)

    context = {
        'alerts': alerts,
        'alerts_json': alerts_json,
    }
    return render(request, 'alerts/home_page.html', context)


# Map view for alerts
def alert_map(request):
    alerts = Alert.objects.filter(published=True).select_related('alert_type')
    alerts_data = []
    for alert in alerts:
        icon_path = alert.alert_type.icon_url if alert.alert_type and alert.alert_type.icon_url else 'images/default-icon.png'
        icon_url = static(icon_path)

        latitude = alert.location.latitude if alert.location else None
        longitude = alert.location.longitude if alert.location else None
        location_name = alert.location.name if alert.location else 'Unknown Location'

        alerts_data.append({
            'title': alert.title,
            'details': alert.details,
            'affected_sites': alert.affected_sites,
            'website_link': alert.website_link,
            'latitude': latitude,
            'longitude': longitude,
            'location': location_name,
            'alert_type': alert.alert_type.name,
            'start_date': alert.start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': alert.end_date.strftime('%Y-%m-%d %H:%M:%S') if alert.end_date else '',
            'icon_url': icon_url,
            'attachment': alert.attachment.url if alert.attachment else '',
            'attachment_name': os.path.basename(alert.attachment.name) if alert.attachment else '',
            'kml_file_url': alert.kml_file.url if alert.kml_file else '',
        })

    alerts_json = json.dumps(alerts_data)
    return render(request, 'alerts/alert_map.html', {'alerts_json': alerts_json})

# View to return JSON data for alerts
def alert_data(request):
    alerts = Alert.objects.filter(published=True).select_related('alert_type')
    alerts_data = []
    for alert in alerts:
        icon_path = alert.alert_type.icon_url if alert.alert_type and alert.alert_type.icon_url else 'images/default-icon.png'
        icon_url = static(icon_path)

        latitude = alert.location.latitude if alert.location else None
        longitude = alert.location.longitude if alert.location else None
        location_name = alert.location.name if alert.location else 'Unknown Location'

        alerts_data.append({
            'title': alert.title,
            'details': alert.details,
            'affected_sites': alert.affected_sites,
            'website_link': alert.website_link,
            'latitude': latitude,
            'longitude': longitude,
            'location': location_name,
            'alert_type': alert.alert_type.name,
            'start_date': alert.start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': alert.end_date.strftime('%Y-%m-%d %H:%M:%S') if alert.end_date else '',
            'icon_url': icon_url,
            'attachment': alert.attachment.url if alert.attachment else '',
            'attachment_name': os.path.basename(alert.attachment.name) if alert.attachment else '',
            'publish_date': alert.publish_date.strftime('%Y-%m-%d %H:%M:%S') if alert.publish_date else '',
            'time_elapsed': alert.time_elapsed,
            'kml_file_url': alert.kml_file.url if alert.kml_file else '',
        })

    return JsonResponse(alerts_data, safe=False)

# Contacts view
def contacts(request):
    return render(request, 'alerts/contacts.html')

# DRF viewset for alerts
class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

# Create alert view for alerts
def create_alert(request):
    if request.method == 'POST':
        form = AlertForm(request.POST, request.FILES)
        if form.is_valid():
            alert = form.save()
            if alert.published:
                send_alert_email(alert)
            return redirect('alert_list')
    else:
        form = AlertForm()
    return render(request, 'alerts/create_alert.html', {'form': form})

# List view for alerts sorted by descending start date
def alert_list(request):
    alerts = Alert.objects.all().select_related('alert_type').order_by('-start_date')
    for alert in alerts:
        alert.time_elapsed = get_time_elapsed(alert.publish_date)
    return render(request, 'alerts/alert_list.html', {'alerts': alerts})

# Send alert email if published
def send_alert_email(alert):
    subject = f"New Alert Published: {alert.title}"
    attachment_link = alert.attachment.url if alert.attachment else ''
    attachment_name = os.path.basename(alert.attachment.name) if alert.attachment else 'No attachment'
    message = f"""
    <html>
        <body>
            <p>A new alert has been published:</p>
            <p><strong>Title:</strong> {alert.title}</p>
            <p><strong>Type:</strong> {alert.alert_type}</p>
            <p><strong>Location:</strong> {alert.location}</p>
            <p><strong>Details:</strong> {alert.details}</p>
            <p><strong>Affected Sites:</strong> {alert.affected_sites}</p>
            <p><strong>Publish Date:</strong> {alert.publish_date}</p>
            <p><strong>Start Date:</strong> {alert.start_date}</p>
            <p><strong>End Date:</strong> {alert.end_date}</p>
            <p><strong>Attachment:</strong> {f'<a href="{settings.BASE_URL}{attachment_link}">{attachment_name}</a>' if alert.attachment else 'No attachment'}</p>
        </body>
    </html>
    """
    email = EmailMessage(subject, message, 'noreply@dbca.wa.gov.au', ['matt.cavana@dbca.wa.gov.au'])
    email.content_subtype = "html"  # Main content is now text/html
    email.send()

# Delete alert view for alerts
@csrf_exempt
def delete_alert(request, alert_id):
    if request.method == 'POST':
        alert = get_object_or_404(Alert, pk=alert_id)
        alert.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

# Unpublish an alert
@csrf_exempt
def unpublish_alert(request):
    if request.method == 'POST':
        alert_id = request.POST.get('id')
        try:
            alert = Alert.objects.get(pk=alert_id)
            if alert.published:
                alert.published = False
                alert.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Alert is already unpublished.'})
        except Alert.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Alert does not exist.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# Test email view - delete if not needed
def test_email(request):
    send_mail(
        'Test Email Subject',
        'Test email body.',
        'noreply@dbca.wa.gov.au',
        ['matt.cavana@dbca.wa.gov.au'],
        fail_silently=False,
    )
    return HttpResponse("Test email sent")

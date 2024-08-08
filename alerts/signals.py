# alerts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Alert

@receiver(post_save, sender=Alert)
def send_alert_email(sender, instance, created, **kwargs):
    if created and instance.published:
        subject = f"New Alert: {instance.title}"
        message = f"""
        Title: {instance.title}
        Details: {instance.details}
        Location: {instance.location}
        Alert Type: {instance.alert_type.name}
        Start Date: {instance.start_date}
        End Date: {instance.end_date}
        """
        send_mail(
            subject,
            message,
            'noreply@dbca.wa.gov.au',
            ['nevilleantonio72@gmail.com'],
            fail_silently=False,
        )

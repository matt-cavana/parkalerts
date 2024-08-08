from django import forms
from .models import Alert, AlertType, Location
from tinymce.widgets import TinyMCE

class AlertForm(forms.ModelForm):
    alert_type = forms.ModelChoiceField(queryset=AlertType.objects.all(), empty_label="Select Alert Type")
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label="Select Location")
    details = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 5}))

    class Meta:
        model = Alert
        fields = ['title', 'alert_type', 'location', 'details', 'affected_sites', 'website_link', 'publish_date', 'start_date', 'end_date', 'published', 'attachment', 'kml_file' ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'publish_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'kml_file': forms.FileInput(attrs={'accept': '.kml'}),
        }

def clean(self):
    cleaned_data = super().clean()
    start_date = cleaned_data.get("start_date")
    end_date = cleaned_data.get("end_date")

    if start_date and end_date and start_date > end_date:
        raise forms.ValidationError("End date should be greater than start date.")
    return cleaned_data

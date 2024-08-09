import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParkAlerts.settings')
django.setup()

from alerts.models import Location

def import_locations_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:  # Using utf-8-sig to handle BOM
        reader = csv.DictReader(csvfile)
        print(f"CSV Headers: {reader.fieldnames}")  # Print headers for debugging
        for row in reader:
            location, created = Location.objects.get_or_create(
                name=row['name'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                contact=row['contact'],
                email=row['email'],
                rprkid=row['rprkid']
            )
            if created:
                print(f"Created new location: {location.name}")
            else:
                print(f"Location already exists: {location.name}")

if __name__ == "__main__":
    file_path = 'locations.csv'  # Update this path if necessary
    import_locations_from_csv(file_path)

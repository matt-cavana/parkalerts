# Generated by Django 4.2.13 on 2024-06-18 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0005_alter_alert_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="alerttype",
            name="icon_url",
            field=models.CharField(max_length=200),
        ),
    ]
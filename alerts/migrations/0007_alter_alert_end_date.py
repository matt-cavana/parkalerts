# Generated by Django 4.2.13 on 2024-07-11 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0006_alter_alerttype_icon_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="alert",
            name="end_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
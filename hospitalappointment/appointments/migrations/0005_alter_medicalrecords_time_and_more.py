# Generated by Django 5.0.1 on 2024-05-05 10:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointments", "0004_alter_medicalrecords_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medicalrecords",
            name="time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 5, 12, 3, 55, 282208)
            ),
        ),
        migrations.AlterField(
            model_name="medicine",
            name="last_modified",
            field=models.DateTimeField(),
        ),
    ]

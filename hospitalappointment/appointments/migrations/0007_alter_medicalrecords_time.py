# Generated by Django 5.0.1 on 2024-05-05 14:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointments", "0006_alter_medicalrecords_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medicalrecords",
            name="time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 5, 16, 43, 26, 560088)
            ),
        ),
    ]

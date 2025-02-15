# Generated by Django 5.0.1 on 2024-05-12 20:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointments", "0012_alter_medicalorder_create_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="claim_rate",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="medicalorder",
            name="create_time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 12, 22, 41, 5, 501293)
            ),
        ),
        migrations.AlterField(
            model_name="medicalrecords",
            name="time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 12, 22, 41, 5, 501293)
            ),
        ),
    ]

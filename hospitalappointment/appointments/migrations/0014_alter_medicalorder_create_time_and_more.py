# Generated by Django 5.0.1 on 2024-05-12 20:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "appointments",
            "0013_customer_claim_rate_alter_medicalorder_create_time_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="medicalorder",
            name="create_time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 12, 22, 56, 41, 317748)
            ),
        ),
        migrations.AlterField(
            model_name="medicalrecords",
            name="time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 12, 22, 56, 41, 313727)
            ),
        ),
    ]

# Generated by Django 4.2.5 on 2024-02-15 21:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("duanolduaempat", "0003_anomalydetection_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="anomalydetection",
            name="is_reported",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="chart",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]

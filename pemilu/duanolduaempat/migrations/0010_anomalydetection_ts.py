# Generated by Django 4.2.5 on 2024-02-20 07:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("duanolduaempat", "0009_backupchasil"),
    ]

    operations = [
        migrations.AddField(
            model_name="anomalydetection",
            name="ts",
            field=models.DateTimeField(blank=True, null=True, verbose_name="version"),
        ),
    ]

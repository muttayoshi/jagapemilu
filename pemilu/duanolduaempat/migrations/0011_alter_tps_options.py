# Generated by Django 4.2.5 on 2024-02-20 10:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("duanolduaempat", "0010_anomalydetection_ts"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tps",
            options={"ordering": ("-created",), "verbose_name_plural": "TPS"},
        ),
    ]

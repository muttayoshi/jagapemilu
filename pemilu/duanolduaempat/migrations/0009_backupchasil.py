# Generated by Django 4.2.5 on 2024-02-19 15:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):
    dependencies = [
        ("duanolduaempat", "0008_administration_ts_chart_ts_image_ts_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BackupCHasil",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                ("kpu_url", models.URLField(blank=True, null=True)),
                ("s3_url", models.URLField(blank=True, null=True)),
                (
                    "img",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="backups", to="duanolduaempat.image"
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
            },
        ),
    ]
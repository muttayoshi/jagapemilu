# Generated by Django 4.2.5 on 2024-02-22 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0006_alter_kecamatan_options_alter_kelurahan_options_and_more"),
        ("duanolduaempat", "0013_image_is_backup"),
    ]

    operations = [
        migrations.AddField(
            model_name="tps",
            name="kelurahan",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tps",
                to="locations.kelurahan",
            ),
        ),
    ]

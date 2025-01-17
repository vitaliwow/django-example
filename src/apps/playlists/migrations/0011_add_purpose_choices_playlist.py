# Generated by Django 4.2.10 on 2024-03-04 18:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('playlists', '0010_change_name_status_to_availability_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='purpose',
            field=models.CharField(
                choices=[('PERSONAL', 'Personal'), ('EDUCATIONAL', 'Educational'), ('COMMERCIAL', 'Commercial')],
                default='COMMERCIAL',
            ),
        ),
    ]
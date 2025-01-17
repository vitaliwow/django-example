# Generated by Django 4.2.11 on 2024-03-05 17:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('playlists', '0011_add_purpose_choices_playlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='purpose',
            field=models.CharField(
                choices=[('PERSONAL', 'Personal'), ('EDUCATIONAL', 'Educational'), ('COMMERCIAL', 'Commercial')],
                default='PERSONAL',
            ),
        ),
    ]
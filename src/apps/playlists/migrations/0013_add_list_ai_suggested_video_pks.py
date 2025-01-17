# Generated by Django 4.2.11 on 2024-05-21 11:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('playlists', '0012_change_default_purpose_playlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='list_ai_suggested_video_pks',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=100), default=list, size=None
            ),
        ),
    ]

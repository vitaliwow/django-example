# Generated by Django 4.2.10 on 2024-03-15 20:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('videos', '0003_remove_uploader'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_unavailable',
            field=models.BooleanField(default=False),
        ),
    ]
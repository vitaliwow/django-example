# Generated by Django 4.2.13 on 2024-06-14 21:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('videos', '0011_add_source_field_for_transcript'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='is_primary',
            field=models.BooleanField(default=True),
        ),
    ]

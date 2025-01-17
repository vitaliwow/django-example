# Generated by Django 4.2.16 on 2024-11-20 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0020_restore_transcript_timings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videofile',
            name='duration',
        ),
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.IntegerField(default=0, help_text='Duration in milliseconds'),
        ),
    ]
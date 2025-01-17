# Generated by Django 4.2.16 on 2024-10-27 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0016_extend_video_and_video_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='quizz_status',
            field=models.CharField(
                choices=[
                    ('NOT_STARTED', 'Not Started'),
                    ('IN_PROGRESS', 'In progress'),
                    ('DONE', 'Done'),
                    ('FAILED', 'Failed'),
                    ('QUEUED', 'QUEUED'),
                ],
                default='NOT_STARTED',
            ),
        ),
        migrations.AddField(
            model_name='video',
            name='short_summary_status',
            field=models.CharField(
                choices=[
                    ('NOT_STARTED', 'Not Started'),
                    ('IN_PROGRESS', 'In progress'),
                    ('DONE', 'Done'),
                    ('FAILED', 'Failed'),
                    ('QUEUED', 'QUEUED'),
                ],
                default='NOT_STARTED',
            ),
        ),
        migrations.AddField(
            model_name='video',
            name='summary_status',
            field=models.CharField(
                choices=[
                    ('NOT_STARTED', 'Not Started'),
                    ('IN_PROGRESS', 'In progress'),
                    ('DONE', 'Done'),
                    ('FAILED', 'Failed'),
                    ('QUEUED', 'QUEUED'),
                ],
                default='NOT_STARTED',
            ),
        ),
        migrations.AddField(
            model_name='video',
            name='transcript_status',
            field=models.CharField(
                choices=[
                    ('NOT_STARTED', 'Not Started'),
                    ('IN_PROGRESS', 'In progress'),
                    ('DONE', 'Done'),
                    ('FAILED', 'Failed'),
                    ('QUEUED', 'QUEUED'),
                ],
                default='NOT_STARTED',
            ),
        ),
    ]

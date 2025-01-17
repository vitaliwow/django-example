# Generated by Django 4.2.15 on 2024-09-16 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('videos', '0014_add_user_and_ordering_for_video_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltranscript',
            name='is_primary',
        ),
        migrations.RemoveField(
            model_name='transcript',
            name='is_primary',
        ),
        migrations.AddField(
            model_name='historicaltranscript',
            name='full_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='historicaltranscript',
            name='raw_data',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='historicaltranscript',
            name='video_file',
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='+',
                to='videos.videofile',
            ),
        ),
        migrations.AddField(
            model_name='transcript',
            name='full_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='transcript',
            name='raw_data',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='transcript',
            name='video_file',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='transcripts',
                to='videos.videofile',
            ),
        ),
        migrations.AddField(
            model_name='videofile',
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
            model_name='videofile',
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
            model_name='videofile',
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
            model_name='videofile',
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
        migrations.AlterField(
            model_name='transcript',
            name='video',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transcripts', to='videos.video'
            ),
        ),
    ]

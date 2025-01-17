# Generated by Django 4.2.16 on 2024-10-23 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0015_extend_video_and_summarization_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='videofile',
            name='video',
            field=models.OneToOneField(
                null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_file', to='videos.video'
            ),
        ),
        migrations.AlterField(
            model_name='video',
            name='source',
            field=models.CharField(
                choices=[('YOUTUBE', 'YouTube'), ('VK', 'VK'), ('UPLOADED', 'Uploaded')], default='YOUTUBE'
            ),
        ),
    ]
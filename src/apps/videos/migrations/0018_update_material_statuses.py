# Generated by Django 4.2.9 on 2024-02-26 08:45

from django.db import migrations


def update_statuses(apps, schema_editor):
    Video = apps.get_model("videos", "Video")
    done = "DONE"

    for video in Video.objects.all():
        if video.transcripts.filter(data__isnull=False).exists():
            video.transcript_status = done
            video.save()


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0017_add_material_status_cook_for_video"),
    ]

    operations = [
        migrations.RunPython(update_statuses, migrations.RunPython.noop),
    ]

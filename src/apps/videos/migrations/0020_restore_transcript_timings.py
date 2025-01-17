from django.db import migrations

def update_transcript_data(apps, schema_editor):
    Transcript = apps.get_model("videos", "Transcript")

    for transcript in Transcript.objects.all():
        if not transcript.data:
            continue

        data = transcript.data
        find_seconds_timing = False

        if "cues" in data:
            for cue in data["cues"]:
                if isinstance(cue.get("start"), (int, float)) and isinstance(cue.get("duration_ms"), (int, float)):
                    cue["start"] = cue["start"] / 1000
                    cue["duration_ms"] = cue["duration_ms"] / 1000
                    find_seconds_timing = True

        if find_seconds_timing:
            transcript.data = data
            transcript.save(update_fields=["data"])

class Migration(migrations.Migration):
    dependencies = [
        ('videos', '0019_update_transcript_timings'),
    ]

    operations = [
        migrations.RunPython(update_transcript_data),
    ]

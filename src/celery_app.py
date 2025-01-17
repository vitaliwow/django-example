import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from core.conf.environ import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings")
app.conf.update(
    broker_url=env("CELERY_BROKER_URL", cast=str, default="redis://redis:6379/0"),
    broker_connection_retry_on_startup=True,
    # by default in debug mode we run all celery tasks in foreground.
    task_always_eager=env("CELERY_TASK_ALWAYS_EAGER", cast=bool, default=settings.DEBUG),
    task_eager_propagates=True,
    task_ignore_result=True,
    task_store_errors_even_if_ignored=True,
    task_acks_late=True,
    timezone=env("TIME_ZONE", cast=str, default="UTC"),
    enable_utc=False,
    beat_schedule={
        "playlists.download_frames_for_commercial_playlists": {
            "task": "playlists.download_frames_for_all_playlists",
            "schedule": crontab(minute="*/30"),
            "options": {"expires": 60 * 120},
        },
        "videos.download_all_transcripts": {
            "task": "videos.download_all_transcripts",
            "schedule": crontab(minute="*/30"),
            "options": {"expires": 60 * 120},
        },
    },
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

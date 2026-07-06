import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.production")

app = Celery("biteplate")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["infrastructure.celery_app"])

app.conf.beat_schedule = {
    "end-of-night-report": {
        "task": "billing.generate_night_report",
        "schedule": crontab(hour=23, minute=59),
    },
}

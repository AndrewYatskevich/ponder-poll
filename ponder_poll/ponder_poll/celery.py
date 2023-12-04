import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ponder_poll.settings")

app = Celery("ponder_poll")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

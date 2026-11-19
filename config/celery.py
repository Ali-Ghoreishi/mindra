import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("mindra")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Discovers Celery task modules, not Django Task models.
app.autodiscover_tasks()
from celery import shared_task
from datetime import datetime


@shared_task
def test_cron_job():
    print(f"Mindra Cron Job executed at {datetime.now()}")
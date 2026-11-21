import logging

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from apps.reminders.locks import acquire_reminder_lock
from apps.reminders.models import Reminder
from apps.reminders.services import send_telegram_message

logger = logging.getLogger(__name__)


@shared_task
def send_reminder(reminder_id):
    lock = acquire_reminder_lock(reminder_id)

    if lock is None:
        logger.info("Reminder %s is already being processed.", reminder_id)
        return

    try:
        try:
            reminder = Reminder.objects.select_related("task").get(id=reminder_id)
        except Reminder.DoesNotExist:
            logger.warning("Reminder %s not found.", reminder_id)
            return

        if reminder.is_sent:
            return

        message = (
            f"🔔 یادآوری وظیفه\n\n"
            f"عنوان: {reminder.task.title}\n"
            f"توضیحات: {reminder.task.description or 'بدون توضیحات'}"
        )

        result = send_telegram_message(
            chat_id=settings.TELEGRAM_CHAT_ID, message=message
        )

        if result.get("ok"):
            reminder.is_sent = True
            reminder.save(update_fields=["is_sent"])
            logger.info("Reminder %s sent successfully.", reminder_id)
        else:
            logger.error("Telegram failed to send reminder %s.", reminder_id)

    finally:
        lock.release()


@shared_task
def dispatch_due_reminders():
    reminder_ids = list(
        Reminder.objects.filter(
            is_sent=False, remind_at__lte=timezone.now()
        ).values_list("id", flat=True)
    )

    for reminder_id in reminder_ids:
        send_reminder.delay(str(reminder_id))

    logger.info("%s reminders dispatched.", len(reminder_ids))

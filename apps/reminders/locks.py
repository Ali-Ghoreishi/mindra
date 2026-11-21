import redis
from django.conf import settings

redis_client = redis.Redis.from_url(settings.REDIS_LOCK_URL, decode_responses=True)


def acquire_reminder_lock(reminder_id):
    lock = redis_client.lock(
        name=f"reminder:lock:{reminder_id}", timeout=60, blocking=False
    )

    acquired = lock.acquire()

    return lock if acquired else None


def release_reminder_lock(lock):
    if lock:
        lock.release()

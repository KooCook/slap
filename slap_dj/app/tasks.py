# Create your Celery tasks here
import time
from contextlib import contextmanager

from celery import shared_task
from celery.exceptions import Reject
from celery.utils.log import get_task_logger
from celery_singleton import Singleton
from django.core.cache import cache

from .models import YouTubeVideo
from .support.billboard_reader import read_billboard_yearly

logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if time.monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)


@shared_task
def add(x, y):
    return x + y


@shared_task
def update_youtube_stats():
    return YouTubeVideo.update_all_video_stats()


@shared_task(base=Singleton)
def xsum(numbers):
    time.sleep(3)
    read_billboard_yearly()
    return sum(numbers)


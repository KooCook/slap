# Create your Celery tasks here
import time
from contextlib import contextmanager

from celery import shared_task
from celery.exceptions import Reject
from celery.utils.log import get_task_logger
from celery_singleton import Singleton
from django.core.cache import cache

from .models import YoutubeVideo


@shared_task
def update_youtube_stats():
    return YoutubeVideo.update_all_video_stats()


import os
import sys

from celery import Celery
from celery.schedules import crontab

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..'))
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slap_dj.settings')

app = Celery('slap_dj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# print(app.conf)

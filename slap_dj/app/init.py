import os

from django.apps import apps
from django.conf import settings


def start_django_lite():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "slap_dj.settings")
    if not apps.loading:
        apps.populate(settings.INSTALLED_APPS)

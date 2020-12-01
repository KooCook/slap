import os

from django.apps import apps
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "slap_dj.slap_dj.settings.flask")
if not apps.loading:
    apps.populate(settings.INSTALLED_APPS)

from slap_flask.models.generator import start_generating

start_generating()

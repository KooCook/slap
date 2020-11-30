import connexion
from connexion import FlaskApp

from slap_flask.database import db
from slap_flask.database.models import load_models
from slap_flask.settings import OPENAPI_SPECS_PATH, OPENAPI_OPS_MODULE_NAME
from connexion.resolver import RestyResolver

import os

from django.apps import apps
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "slap_dj.slap_dj.settings.flask")
if not apps.loading:
    apps.populate(settings.INSTALLED_APPS)

from slap_flask.views import root


def create_app() -> FlaskApp:
    connexion_app = connexion.App(__name__, specification_dir='swagger', options={"swagger_ui": True})
    connexion_app.add_api(OPENAPI_SPECS_PATH, resolver=RestyResolver(OPENAPI_OPS_MODULE_NAME))
    connexion_app.app.register_blueprint(root)
    return connexion_app


if __name__ == '__main__':
    app = create_app()
    db.connect_app(app.app)
    load_models(app.app)
    # start_generating()
    app.run(port=8080, debug=True)

import connexion
from connexion import FlaskApp
from flask import Flask

from slap_flask.settings import OPENAPI_SPECS_PATH, OPENAPI_OPS_MODULE_NAME
from connexion.resolver import RestyResolver
from slap_flask.views import root


def create_app() -> FlaskApp:
    connexion_app = connexion.App(__name__, specification_dir='swagger', options={"swagger_ui": True})

    connexion_app.add_api(OPENAPI_SPECS_PATH, resolver=RestyResolver(OPENAPI_OPS_MODULE_NAME))
    connexion_app.app.register_blueprint(root)
    return connexion_app


if __name__ == '__main__':
    app = create_app()
    app.run(port=8080, debug=True)

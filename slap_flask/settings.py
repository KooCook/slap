from decouple import config
from flask import Flask

from dirs import ROOT_DIR


MODULE_NAME = "slap_flask"
OPENAPI_OPS_MODULE_NAME = "slap_flask.public.controllers"
RELATIVE_DIR = ROOT_DIR / MODULE_NAME

OPENAPI_SPECS_PATH = RELATIVE_DIR / config("OPENAPI_SPECS_PATH", default="openapi.yaml")
DATABASE_URI = config("DATABASE_URI", default="sqlite:///slap.sqlite")


# def init_config(app: Flask):
#     app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI


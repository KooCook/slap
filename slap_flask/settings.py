from decouple import config

from dirs import ROOT_DIR


MODULE_NAME = "slap_flask"
OPENAPI_OPS_MODULE_NAME = "slap_flask.public.controllers"
RELATIVE_DIR = ROOT_DIR / MODULE_NAME

OPENAPI_SPECS_PATH = RELATIVE_DIR / config("OPENAPI_SPECS_PATH", default="openapi.yaml")

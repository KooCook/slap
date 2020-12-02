from decouple import config, Csv
from dirs import ROOT_DIR

YOUTUBE_DATA_API_KEYS = config("YOUTUBE_DATA_API_KEYS", cast=Csv(), default="")
GENIUS_SECRET = config("GENIUS_SECRET", default="")
SPOTIFY_CLIENT_ID = config("SPOTIFY_CLIENT_ID", default="")
SPOTIFY_CLIENT_SECRET = config("SPOTIFY_CLIENT_SECRET", default="")
MODULE_NAME = "slap_flask"
OPENAPI_OPS_MODULE_NAME = "slap_flask.public.controllers"
RELATIVE_DIR = ROOT_DIR / MODULE_NAME

OPENAPI_SPECS_PATH = RELATIVE_DIR / config("OPENAPI_SPECS_PATH", default="openapi.yaml")
DATABASE_URI = config("DATABASE_URI", default="sqlite:///slap.sqlite")

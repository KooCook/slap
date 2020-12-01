from decouple import config, Csv

YOUTUBE_DATA_API_KEYS = config("YOUTUBE_DATA_API_KEYS", cast=Csv())

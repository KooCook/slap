from celery.schedules import crontab

BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Bangkok'
CELERYBEAT_SCHEDULE = {
    'context': {
        'task': 'app.tasks.xsum',
        'schedule': crontab(minute=1),
        'args': ((4, 5),)
    },
    'yt_task': {
        'task': 'app.tasks.update_youtube_stats',
        'schedule': crontab(minute=5),
        'args': ()
    }
}
CELERYBEAT_MAX_LOOP_INTERVAL = 1

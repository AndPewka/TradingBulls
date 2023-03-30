from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    'update_currency': {
        'task': 'workers.update_currency.update_currency',
        'schedule': timedelta(minutes=1),
    },
}

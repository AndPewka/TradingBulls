from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    'update_currency': {
        'task': 'workers.update_currency.update_currency',
        'schedule': timedelta(minutes=1),
    },
    'update_rsi': {
        'task': 'workers.update_currency.update_rsi',
        'schedule': timedelta(minutes=1),
    },
}

from datetime import datetime, timedelta

CELERY_BEAT_SCHEDULE = {
    'print_hello_world_1': {
        'task': 'workers.update_currency.print_hello_world_1',
        'schedule': timedelta(seconds=5),
    },

    'print_hello_world_2': {
        'task': 'workers.update_currency.print_hello_world_2',
        'schedule': timedelta(seconds=1),
    },
}
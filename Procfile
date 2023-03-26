docker: docker-compose up
web: python manage.py runserver localhost:8000
app-telegram-bot: python manage.py bot
celery-beats: celery -A config beat --loglevel=info
celery-worker: celery -A config worker --loglevel=info

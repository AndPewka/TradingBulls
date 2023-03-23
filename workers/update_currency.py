from celery import shared_task, Celery
from datetime import datetime, timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

@shared_task
def print_hello_world_1():
    print("Hello, World!11111111111111")

@shared_task
def print_hello_world_2():
    print("Hello, World!22222222222222")
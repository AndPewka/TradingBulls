import itertools
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.management.utils import get_random_secret_key
from django.core.management import execute_from_command_line
from dotenv import set_key, load_dotenv, dotenv_values
from django.apps import apps
from django import setup
import psycopg2

setup()
load_dotenv()

DEFAULT_SERVICES = ["Binance"]
DEFAULT_CURRENCY = ["ETHUSDT", "BTCUSDT"]

Client = apps.get_model("telegram_bot", "Client", require_ready=True)
Service = apps.get_model("telegram_bot", "Service", require_ready=True)
CurrencyPair = apps.get_model("telegram_bot", "CurrencyPair", require_ready=True)


def generate_default_currency():
    for service, currency in itertools.product(DEFAULT_SERVICES, DEFAULT_CURRENCY):
        service_obj, created = Service.objects.get_or_create(title=service, api_class_name=service)
        _, created = CurrencyPair.objects.get_or_create(
            service=service_obj,
            name=currency,
            state=CurrencyPair.States.active
        )

        if created:
            print(f"create pair {currency} on {service}")


def create_developer_client():
    client, created = Client.objects.get_or_create(login=os.getenv('DJANGO_USERNAME'),
                                                   email="admin@example.com",
                                                   password=os.getenv('DJANGO_PASSWORD'),
                                                   password_hash=os.getenv('DJANGO_PASSWORD'))
    if created:
        print(f"create developer client")
    
    api_keys = {}
    env_vars = dotenv_values('.env')

    for service in DEFAULT_SERVICES:
        pattern = re.compile(rf'{service.upper()}')
        keys = [key for key in env_vars.keys() if pattern.match(key)]

        for key in keys:
            api_keys.setdefault(service.lower(), {})[key.split(service.upper() + "_")[1]] = env_vars[key]
    
    client.api_parameters = api_keys
    client.save()


def create_super_user():
    from django.contrib.auth.models import User
 
    username = os.getenv('DJANGO_USERNAME')
    password = os.getenv('DJANGO_PASSWORD')
    email = "admin@example.com"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print('Superuser created successfully.')


def generate_django_secret():
    if os.getenv('DJANGO_SECRET_KEY'):
        return False

    print("create DJANGO_SECRET_KEY")
    set_key('.env', 'DJANGO_SECRET_KEY', get_random_secret_key())


def create_postgres_db():
    conn = psycopg2.connect(dbname='postgres',
                            user=os.getenv('POSTGRES_USER'),
                            password=os.getenv('POSTGRES_PASSWORD'),
                            host=os.getenv('PG_ADDRESS'),
                            port=os.getenv('PG_PORT'))
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
    databases = [row[0] for row in cursor.fetchall()]

    if os.getenv('POSTGRES_DB') not in databases:
        print(f"create postgres db {os.getenv('POSTGRES_DB')}")
        cursor.execute(f"CREATE DATABASE {os.getenv('POSTGRES_DB')}")


def migrate_postgres_db():
    execute_from_command_line(['manage.py', 'migrate'])


if __name__ == '__main__':
    create_postgres_db()
    migrate_postgres_db()
    create_super_user()
    generate_default_currency()
    create_developer_client()
    generate_django_secret()

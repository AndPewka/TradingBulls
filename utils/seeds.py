import sys
import os
import itertools

from django import setup
from django.apps import apps
from django.core.management.utils import get_random_secret_key
from dotenv import set_key, load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
setup()
load_dotenv()

def generate_default_currency():
    Service = apps.get_model("telegram_bot", "Service", require_ready=True)
    CurrencyPair = apps.get_model("telegram_bot", "CurrencyPair", require_ready=True)

    default_currency = ["ETHUSDT", "BTCUSDT"]
    default_services= ["Binance"]

    for service, currency in itertools.product(default_services, default_currency):
        service_obj, created = Service.objects.get_or_create(title=service, api_class_name=service)
        _, created = CurrencyPair.objects.get_or_create(service=service_obj, name=currency, state=CurrencyPair.States.active)
        if created:
            print(f"create pair {currency} on {service}")

def generate_django_secret():
    if os.getenv('DJANGO_SECRET_KEY'):
        return False

    print(f"create DJANGO_SECRET_KEY")
    set_key('.env', 'DJANGO_SECRET_KEY', get_random_secret_key())

if __name__ == '__main__':
    generate_default_currency()
    generate_django_secret()

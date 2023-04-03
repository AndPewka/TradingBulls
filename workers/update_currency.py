import datetime as dt
import os

import django
from dateutil.tz import tzlocal
from influxdb_client import Point
from celery import shared_task
from django.apps import apps
import itertools

from lib.trading_platforms_api import *
from lib.influxdb import Wrapper
from lib.indicators.rsi import RSI

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

Service = apps.get_model("telegram_bot", "Service", require_ready=True)
CurrencyPair = apps.get_model("telegram_bot", "CurrencyPair", require_ready=True)
Rsi = apps.get_model("telegram_bot", "Rsi", require_ready=True)


@shared_task
def update_currency():
    services = Service.objects.all()
    influx = Wrapper()
    print(f"Services count: {len(services)}")

    for service in services:
        print(f"Starting updates for {service}.")
        api = globals()[service.api_class_name]()
        pairs = CurrencyPair.objects.filter(service=service, state=CurrencyPair.States.active)
        print(f"Pairs count for {service}: {len(pairs)}")

        for pair in pairs:
            print(f"Updating {pair}.")
            query = influx.gen_query().\
                           range(15, unit="d").\
                           measurement("currency").\
                           filter(service=service.title, currency_pair=pair.name, _field="close_price").\
                           last()

            last_entry = influx.query(query())

            last_entry_time = next(
                iter(last_entry),
                {"_time": dt.datetime.now(tzlocal()) - dt.timedelta(days=15)}
            )["_time"]

            time_passed_from_last_entry = dt.datetime.now(tzlocal()) - last_entry_time
            print(f"Time passed from last entry: {time_passed_from_last_entry}")

            days = time_passed_from_last_entry.days
            hours = time_passed_from_last_entry.seconds // 3600
            minutes = time_passed_from_last_entry.seconds % 3600 // 60

            if not any([days, hours, minutes]):
                print("Noting to update.")
                continue

            try:
                result = api.get_history(pair.name, days=days, hours=hours, minutes=minutes)
            except ValueError as error:
                print(f"{error}\nDisabling pair {pair}.")
                pair.state = CurrencyPair.States.disabled
                pair.save()
                continue

            batch = [
                Point.from_dict({
                    "measurement": "currency",
                    "tags": {
                        "service": service.title,
                        "currency_pair": pair.name,
                    },
                    "time": res.pop("time"),
                    "fields": res
                }) for res in result
            ]
            influx.write_batch(batch)

            print(f"Batch size: {len(batch)}")


@shared_task
def update_rsi():
    devault_intervals = [1, 5, 10, 15, 25, 30, 60]
    services = Service.objects.all()

    influx = Wrapper()
    pairs = CurrencyPair.objects.filter(state=CurrencyPair.States.active)

    for pair, interval in itertools.product(pairs, devault_intervals):
        value = RSI().calculate(service=pair.service.title,
                                symbol=pair.name,
                                interval=interval,
                                period=3).last()
        
        influx.write(measurement="rsi", tags={"interval": f"{interval}m", "currency_pair": pair.name}, fields={"rate": value})
            

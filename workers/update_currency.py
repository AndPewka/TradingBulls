from os import getenv
from time import sleep

from redis import Redis
from celery import shared_task, group

from lib.trading_platforms_api import *
from lib.errors import NoSuchServiceError
from apps.telegram_bot.models import CurrencyPair

# TODO: Не проверял пока на работоспособность.


class UpdateCurrencyWorker:
    def __init__(self, service):
        try:
            service_class = globals()[service]
        except KeyError:
            raise NoSuchServiceError(service)

        self.service = service
        self.api = service_class()

        address, port, password = getenv("REDIS_ADDRESS"), getenv("REDIS_PORT"), getenv("REDIS_PASSWORD")
        self.redis = Redis(host=address, port=port, password=password)

    @shared_task
    def update_currency_rate(self, symbol, interval):
        while True:
            # Получаем курс + время
            currency = self.api.get_currency(symbol)

            # Добавляем в redis запись по ключу currency:service:symbol
            self.redis.zadd(f"currency:{self.service}:{symbol}", {currency["value"]: currency["time"]})

            sleep(interval)

    @classmethod
    def init_tasks(cls):
        """
        Функция для запуска тасок на обновление курса.
        Для инициализации всех тасок просто вызвать UpdateCurrencyWorker.init_tasks()
        """

        # Берем существующие в админке сервисы из модельки CurrencyPair
        services = CurrencyPair.objects.values('service').distinct()

        # Создаем экземпляры классов сгруппировав по сервису
        workers_by_service = {service: cls(service) for service in services}

        for service, worker in workers_by_service.items():
            # Ищем какие пары валют есть в админке для текущего сервиса
            symbols = CurrencyPair.objects.filter(service=service).values('name').all()

            # Создаем таски для каждой валютной пары
            tasks = [worker.update_currency_rate.s(symbol, interval=15) for symbol in symbols]

            # Запускаем группу задач
            group(tasks).apply_async()

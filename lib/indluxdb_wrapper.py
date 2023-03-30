import os
from datetime import datetime

from influxdb_client import InfluxDBClient
from dotenv import load_dotenv

load_dotenv()


class InfluxdbWrapper:
    """Удобный wrapper influxdb-клиента"""

    def __init__(self, org=None, bucket=None):
        self.url = f"http://{os.getenv('INFLUXDB_ADDRESS')}:{os.getenv('INFLUXDB_PORT')}"
        self.token = os.getenv("INFLUXDB_API_TOKEN")
        self.org = org or os.getenv("INFLUXDB_ORG_NAME")
        self.bucket = bucket or os.getenv("INFLUXDB_BUCKET_NAME")

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org,
            bucket=self.bucket
        )
        self.query_api = self.client.query_api()
        self.write_api = self.client.write_api()

    def write(self, measurement, tags=None, fields=None, timestamp=None):
        """
        Одна запись в измерение measurement

        :param measurement: [str]           - измерение
        :param tags:        [dict, None]    - тэги в формате словаря
        :param fields:      [dict, None]    - поля в формате словаря
        :param timestamp:   [datetime]      - время записи в формате datetime
        :return: result
        """
        timestamp = timestamp or datetime.utcnow()

        self.write_api.write(
            org=self.org,
            bucket=self.bucket,
            record=[{
                "measurement": measurement,
                "tags": tags,
                "fields": fields,
                "time": timestamp
            }]
        )

    def write_batch(self, points, flush_interval=1000):
        """
        Записать batch данных в базу. Для этой функции нужно вручную создать нужные записи с помощью класса Point

        :param points:          [list<Point>]   - тэги в формате словаря
        :param flush_interval:  [int]           - flush_interval для write_api
        :return: result
        """
        self.client.write_api(batch_size=len(points), flush_interval=flush_interval).\
                    write(org=self.org, bucket=self.bucket, record=points)

    def get_from_measurement(
            self,
            measurement,
            last_hours=24,
            filters=None,
            keep_tags=None,
            desc=False,
            limit=None,
            group_by_minutes=None,
            aggregate_function=None,
            debug=False,
    ):
        """
        Простой query-запрос с получением данных из бд
        Для более сложных можно написать свой query-запрос на языке flux и выполнить с помощью метода query
        Функционал расширяется

        :param measurement:       [str]        - таблица с измерениями
        :param last_hours:        [int]        - фильтр по времени (берутся записи за последние last_hours часов)
        :param filters:           [dict, None] - дополнительные фильтры в виде словаря (<тег/поле>: <значение>)
        :param keep_tags:         [list, None] - список тэгов, которые нужно оставить в результате
        :param desc:              [bool]       - сортировка desc
        :param limit:             [int, None]  - ограничение по количеству записей
        :param group_by_minutes   [int, None]  - количество минут для группировки, обязательно с aggregate_function
        :param aggregate_function [str, None]  - аггрегирующая функция (first, last, distinct и т.п.)
        :param debug:             [bool]       - при значении True печатается query запрос
        :return:                  [list[dict]] - список совпадающиих записей из бд в формате словаря
        """

        keep_string = '|> keep(columns: ' + self.stringify(
            ["_field", "_value", "_time"] + keep_tags
        ) + ")" if keep_tags else ''
        filter_string = '|> filter(fn: (r) => ' + " and ".join(
            [f'r["{key}"] == "{value}"' for key, value in filters.items()]
        ) + ")" if filters else ""
        order_string = f'|> sort(columns: ["_time"], desc: true)' if desc else ''
        limit_string = f'|> limit(n: {limit})' if limit else ''

        match (aggregate_function, group_by_minutes):
            case None | "", _:
                aggregate_string = ''
            case _, None | "":
                aggregate_string = f'|> {aggregate_function}()'
            case _:
                aggregate_string = f'|> aggregateWindow(every: {group_by_minutes}m, fn: {aggregate_function})'

        raw_query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -{last_hours}h)
          |> filter(fn: (r) => r["_measurement"] == "{measurement}")
          {filter_string}
          {keep_string}
          {order_string}
          {limit_string}
          {aggregate_string}
        '''
        query = "\n".join([line for line in raw_query.split("\n") if line.strip()])

        if debug:
            print(f"Executing query:\n{query}")

        result = self.query(query)

        if not result:
            return []

        return [res.values for res in self.query(query)[0].records]

    def query(self, query):
        """
        Query-запрос в influxdb.
        Когда функционала метода get_from_measurement недостаточно для составления запроса,
        можно написать собственный запрос с использованием языка Flux

        :param query:   [str]   - query-запрос на языке Flux
        :return result
        """
        return self.query_api.query(query, org=self.org)

    @staticmethod
    def stringify(obj):
        return str(list(obj)).replace("'", '"')

    @staticmethod
    def generate_aggregate_string(group_by_minutes, aggregate_function):
        if not aggregate_function:
            return ''

        if group_by_minutes:
            return f'|> aggregateWindow(every: {group_by_minutes}m, fn: {aggregate_function})'

        else:
            return f'|> {aggregate_function}()'